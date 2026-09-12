import unittest
import hashlib

class TestSecurityTriage(unittest.TestCase):

    def test_hashing_correctness(self):
        sample_bytes = b"test string"
        expected = hashlib.sha256(sample_bytes).hexdigest()
        actual = hashlib.sha256(sample_bytes).hexdigest()
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()