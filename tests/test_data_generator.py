import unittest
from src.data.data_generator import generate_heartbeat

class TestDataGenerator(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
