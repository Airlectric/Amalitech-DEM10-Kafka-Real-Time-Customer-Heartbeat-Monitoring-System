import unittest
from src.data.data_generator import generate_heartbeat

    def test_generate_heartbeat_fields(self):
        hb = generate_heartbeat()
        self.assertIn('customer_id', hb)
        self.assertIn('timestamp', hb)
        self.assertIn('heart_rate', hb)
        self.assertIn('valid', hb)

    def test_heartbeat_validity(self):
        # Run multiple times to check both valid and invalid
        found_valid = found_invalid = False
        for _ in range(100):
            hb = generate_heartbeat()
            if hb['valid']:
                found_valid = True
            else:
                found_invalid = True
        self.assertTrue(found_valid)
        self.assertTrue(found_invalid)

    unittest.main()

    def test_generate_heartbeat_fields(self):
        hb = generate_heartbeat()
        self.assertIn('patient_id', hb)
        self.assertIn('timestamp', hb)
        self.assertIn('heartbeat_value', hb)
        self.assertIn('status', hb)

    def test_heartbeat_status(self):
        found_valid = found_invalid_low = found_invalid_high = False
        for _ in range(100):
            hb = generate_heartbeat()
            if hb['status'] == 'valid':
                found_valid = True
            elif hb['status'] == 'invalid_low':
                found_invalid_low = True
            elif hb['status'] == 'invalid_high':
                found_invalid_high = True
        self.assertTrue(found_valid)
        self.assertTrue(found_invalid_low)
        self.assertTrue(found_invalid_high)


class TestDataGenerator(unittest.TestCase):
    def test_generate_heartbeat_fields(self):
        hb = generate_heartbeat()
        self.assertIn('patient_id', hb)
        self.assertIn('timestamp', hb)
        self.assertIn('heartbeat_value', hb)

    def test_heartbeat_value_range(self):
        # Run multiple times to check for both valid and invalid
        found_valid = found_invalid = False
        for _ in range(100):
            hb = generate_heartbeat()
            if 50 <= hb['heartbeat_value'] <= 120:
                found_valid = True
            else:
                found_invalid = True
        self.assertTrue(found_valid)
        self.assertTrue(found_invalid)

if __name__ == "__main__":
    unittest.main()
if __name__ == "__main__":
    unittest.main()
