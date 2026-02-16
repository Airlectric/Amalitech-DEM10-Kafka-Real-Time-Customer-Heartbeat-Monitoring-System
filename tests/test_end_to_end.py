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
        """Test complete data flow: produce → consume → store (new schema)"""
        # Get initial count
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM heartbeats")
                initial_heartbeats = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM heartbeat_alerts")
                initial_alerts = cur.fetchone()[0]
        finally:
            put_connection(conn)

        # Start producer in background (using module syntax)
        producer = subprocess.Popen(
            ['python', '-m', 'src.main', '--producer'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Start consumer in background
        consumer = subprocess.Popen(
            ['python', '-m', 'src.main', '--consumer'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        try:
            # Let them run for 5 seconds
            time.sleep(5)

            # Stop processes
            producer.send_signal(signal.SIGTERM)
            consumer.send_signal(signal.SIGTERM)
            producer.wait(timeout=5)
            consumer.wait(timeout=5)
        finally:
            # Ensure processes are terminated and resources released
            if producer.poll() is None:
                producer.kill()
                producer.wait()
            if consumer.poll() is None:
                consumer.kill()
                consumer.wait()

        # Wait a bit for final inserts
        time.sleep(2)

        # Check if records were added
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM heartbeats")
                final_heartbeats = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM heartbeat_alerts")
                final_alerts = cur.fetchone()[0]

                self.assertGreater(final_heartbeats, initial_heartbeats, "No heartbeat events were added")
                self.assertGreaterEqual(final_alerts, initial_alerts, "Alert count did not increase (may be zero if no invalid events)")

                print(f"\nHeartbeats: {initial_heartbeats} -> {final_heartbeats} (+{final_heartbeats - initial_heartbeats})")
                print(f"Alerts: {initial_alerts} -> {final_alerts} (+{final_alerts - initial_alerts})")
        finally:
            put_connection(conn)
    
    def test_database_schema(self):
        """Test that required tables exist (new schema)"""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = [row[0] for row in cur.fetchall()]
                self.assertIn('heartbeats', tables)
                self.assertIn('heartbeat_alerts', tables)
        finally:
            put_connection(conn)
    

    def test_data_validation(self):
        """Test that validation logic works correctly (new schema)"""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Check that all 'valid' status heartbeats are within range
                cur.execute("""
                    SELECT COUNT(*) FROM heartbeats 
                    WHERE validation_status = 'valid' AND (heartbeat_value < 50 OR heartbeat_value > 120)
                """)
                invalid_in_valid = cur.fetchone()[0]
                self.assertEqual(invalid_in_valid, 0, "Invalid heartbeats found with status 'valid'")
        finally:
            put_connection(conn)

if __name__ == '__main__':
    unittest.main()
