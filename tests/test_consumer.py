import unittest
from unittest.mock import patch, MagicMock
from src.kafka import consumer

class TestConsumer(unittest.TestCase):
    @patch('src.kafka.consumer.consumer')
    @patch('src.kafka.consumer.insert_valid_heartbeat')
    @patch('src.kafka.consumer.insert_invalid_heartbeat')
    def test_consumer_processes_messages(self, mock_invalid, mock_valid, mock_consumer):
        # Simulate two messages: one valid, one invalid
        valid_msg = MagicMock()
        valid_msg.value = {'customer_id': 'A', 'timestamp': '2024-01-01T00:00:00', 'heart_rate': 80}
        invalid_msg = MagicMock()
        invalid_msg.value = {'customer_id': 'B', 'timestamp': '2024-01-01T00:00:00', 'heart_rate': 10}
        mock_consumer.poll.return_value = {None: [valid_msg, invalid_msg]}
        with patch('src.kafka.consumer.validate_heartbeat', side_effect=[(True, None), (False, 'Heart rate out of range: 10')]):
            with patch('src.kafka.consumer.consumer.commit') as mock_commit:
                with patch('src.kafka.consumer.consumer.close'):
                    with self.assertRaises(KeyboardInterrupt):
                        def side_effect(*args, **kwargs):
                            raise KeyboardInterrupt()
                        mock_consumer.poll.side_effect = side_effect
                        consumer.main()
        mock_valid.assert_called()
        mock_invalid.assert_called()

if __name__ == "__main__":
    unittest.main()
