"""
End-to-End Test for Heartbeat Monitoring System
Tests the complete data flow from generator to database
"""

import unittest
import time
import subprocess
import signal
import os
from src.db.db_utils import get_connection, put_connection

class TestEndToEnd(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Check if infrastructure is running"""
        # Check Docker containers
        result = subprocess.run(
            ['docker', 'compose', 'ps', '--format', 'table'],
            capture_output=True, text=True
        )
        if 'postgres' not in result.stdout or 'kafka' not in result.stdout:
            raise Exception("Infrastructure not running. Run: docker compose up -d")
    
    def test_data_flow(self):
        """Test complete data flow: produce → consume → store"""
        # Get initial count
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM heartbeats_valid")
                initial_valid = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM heartbeats_invalid")
                initial_invalid = cur.fetchone()[0]
        finally:
            put_connection(conn)
        
        # Start producer in background
        producer = subprocess.Popen(
            ['python', 'src/main.py', '--producer'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Start consumer in background
        consumer = subprocess.Popen(
            ['python', 'src/main.py', '--consumer'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Let them run for 5 seconds
        time.sleep(5)
        
        # Stop processes
        producer.send_signal(signal.SIGTERM)
        consumer.send_signal(signal.SIGTERM)
        producer.wait()
        consumer.wait()
        
        # Wait a bit for final inserts
        time.sleep(2)
        
        # Check if records were added
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM heartbeats_valid")
                final_valid = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM heartbeats_invalid")
                final_invalid = cur.fetchone()[0]
                
                # Assert records were added
                self.assertGreater(final_valid, initial_valid, 
                    "No valid records were added")
                self.assertGreater(final_invalid, initial_invalid, 
                    "No invalid records were added")
                
                print(f"\nValid records: {initial_valid} → {final_valid} "
                      f"(+{final_valid - initial_valid})")
                print(f"Invalid records: {initial_invalid} → {final_invalid} "
                      f"(+{final_invalid - initial_invalid})")
        finally:
            put_connection(conn)
    
    def test_database_schema(self):
        """Test that required tables exist"""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = [row[0] for row in cur.fetchall()]
                
                self.assertIn('heartbeats_valid', tables)
                self.assertIn('heartbeats_invalid', tables)
        finally:
            put_connection(conn)
    
    def test_data_validation(self):
        """Test that validation logic works correctly"""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Check that heart_rate in valid table is within range
                cur.execute("""
                    SELECT COUNT(*) FROM heartbeats_valid 
                    WHERE heart_rate < 50 OR heart_rate > 120
                """)
                invalid_in_valid = cur.fetchone()[0]
                self.assertEqual(invalid_in_valid, 0, 
                    "Invalid heart rates found in valid table")
        finally:
            put_connection(conn)

if __name__ == '__main__':
    unittest.main()
