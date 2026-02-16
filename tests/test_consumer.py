import unittest
from unittest.mock import patch, MagicMock


from src.kafka.consumer import classify_heartbeat

class TestConsumer(unittest.TestCase):
    def test_classify_heartbeat_valid(self):
        event = {'heartbeat_value': 75}
        result = classify_heartbeat(event)
        self.assertEqual(result['validation_status'], 'valid')
        self.assertIsNone(result['anomaly_type'])
        self.assertIsNone(result['alert_category'])

    def test_classify_heartbeat_low_bpm(self):
        event = {'heartbeat_value': 30}
        result = classify_heartbeat(event)
        self.assertEqual(result['validation_status'], 'invalid_physiological')
        self.assertEqual(result['anomaly_type'], 'low_bpm')
        self.assertEqual(result['alert_category'], 'physiological_anomaly')

    def test_classify_heartbeat_high_bpm(self):
        event = {'heartbeat_value': 150}
        result = classify_heartbeat(event)
        self.assertEqual(result['validation_status'], 'invalid_physiological')
        self.assertEqual(result['anomaly_type'], 'high_bpm')
        self.assertEqual(result['alert_category'], 'physiological_anomaly')

    def test_classify_heartbeat_negative(self):
        event = {'heartbeat_value': -10}
        result = classify_heartbeat(event)
        self.assertEqual(result['validation_status'], 'invalid_system')
        self.assertEqual(result['anomaly_type'], 'negative_value')
        self.assertEqual(result['alert_category'], 'system_anomaly')

    def test_classify_heartbeat_null(self):
        event = {'heartbeat_value': None}
        result = classify_heartbeat(event)
        self.assertEqual(result['validation_status'], 'invalid_system')
        self.assertEqual(result['anomaly_type'], 'null_value')
        self.assertEqual(result['alert_category'], 'system_anomaly')

    def test_classify_heartbeat_parsing_error(self):
        event = {'heartbeat_value': 'not_a_number'}
        result = classify_heartbeat(event)
        self.assertEqual(result['validation_status'], 'corrupted')
        self.assertEqual(result['anomaly_type'], 'parsing_error')
        self.assertEqual(result['alert_category'], 'data_corruption')

if __name__ == "__main__":
    unittest.main()
