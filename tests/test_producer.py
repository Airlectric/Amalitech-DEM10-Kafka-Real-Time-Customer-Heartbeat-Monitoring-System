import unittest
from unittest.mock import patch, MagicMock
from src.data.data_generator import generate_heartbeat



class TestProducer(unittest.TestCase):
    def test_generate_heartbeat_structure(self):
        """Test that data generator creates correct structure for producer"""
        event = generate_heartbeat()
        self.assertIn('patient_id', event)
        self.assertIn('timestamp', event)
        self.assertIn('heartbeat_value', event)

if __name__ == "__main__":
    unittest.main()
