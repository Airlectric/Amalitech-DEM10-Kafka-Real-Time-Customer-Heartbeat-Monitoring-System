import unittest
from unittest.mock import patch
from src.kafka import producer

class TestProducer(unittest.TestCase):
    @patch('src.kafka.producer.producer')
    @patch('src.kafka.producer.generate_heartbeat')
    def test_producer_sends_heartbeat(self, mock_generate, mock_producer):
        mock_generate.return_value = {
            'customer_id': 'TEST1234',
            'timestamp': '2024-01-01T00:00:00',
            'heart_rate': 80,
            'valid': True
        }
        with patch('time.sleep', return_value=None):
            with self.assertRaises(KeyboardInterrupt):
                # Simulate KeyboardInterrupt after one send
                def side_effect(*args, **kwargs):
                    raise KeyboardInterrupt()
                mock_producer.send.side_effect = side_effect
                producer.main()
        mock_producer.send.assert_called()

if __name__ == "__main__":
    unittest.main()
