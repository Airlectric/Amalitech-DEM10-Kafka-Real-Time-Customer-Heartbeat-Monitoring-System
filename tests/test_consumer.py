import unittest
from unittest.mock import patch, MagicMock
from src.kafka.consumer import validate_heartbeat
from src.config.config import HEART_RATE_MIN, HEART_RATE_MAX

class TestConsumer(unittest.TestCase):
    def test_validate_heartbeat_valid(self):
        """Test validation accepts valid heart rates"""
        valid_data = {'heart_rate': 75}
        is_valid, reason = validate_heartbeat(valid_data)
        self.assertTrue(is_valid)
        self.assertIsNone(reason)
    
    def test_validate_heartbeat_invalid_low(self):
        """Test validation rejects heart rate too low"""
        invalid_data = {'heart_rate': 30}
        is_valid, reason = validate_heartbeat(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn('out of range', reason)
    
    def test_validate_heartbeat_invalid_high(self):
        """Test validation rejects heart rate too high"""
        invalid_data = {'heart_rate': 150}
        is_valid, reason = validate_heartbeat(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn('out of range', reason)
    
    def test_validate_heartbeat_missing(self):
        """Test validation handles missing heart_rate"""
        invalid_data = {'customer_id': 'TEST'}
        is_valid, reason = validate_heartbeat(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn('Missing', reason)

if __name__ == "__main__":
    unittest.main()
