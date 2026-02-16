import unittest
from unittest.mock import patch, MagicMock
from src.data.data_generator import generate_heartbeat

class TestProducer(unittest.TestCase):
    def test_generate_heartbeat_structure(self):
        """Test that data generator creates correct structure for producer"""
        heartbeat = generate_heartbeat()
        self.assertIn('customer_id', heartbeat)
        self.assertIn('timestamp', heartbeat)
        self.assertIn('heart_rate', heartbeat)
        self.assertIn('valid', heartbeat)

if __name__ == "__main__":
    unittest.main()
