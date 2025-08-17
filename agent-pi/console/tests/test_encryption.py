import unittest
from utility.encryption import compare_password
from werkzeug.security import generate_password_hash

class TestInputValidation(unittest.TestCase):
    def test_validate_input(self):
        # Test valid hash
        test_hash = generate_password_hash("test", method="pbkdf2:sha256", salt_length=16)
        self.assertTrue(compare_password("test", test_hash))

        # Test invalid hash
        test_hash = generate_password_hash("test_wrong", method="pbkdf2:sha256", salt_length=16)
        self.assertFalse(compare_password("test", test_hash))
        
        # Test invalid password
        test_hash = generate_password_hash("test", method="pbkdf2:sha256", salt_length=16)
        self.assertFalse(compare_password("test_wrong", test_hash))
        
if __name__ == '__main__':
    unittest.main()
        
        
        