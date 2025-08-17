import unittest
from utility.input_validation import validate_input, validate_email


class TestInputValidation(unittest.TestCase):
    def test_validate_input(self):
        # Test valid input
        self.assertTrue(validate_input("test"))

        # Test invalid input
        self.assertFalse(validate_input(""))

    def test_validate_email(self):
        # Test valid email
        self.assertTrue(validate_email("test@example.com"))

        # Test invalid email
        self.assertFalse(validate_email("test@.com"))
        
        
if __name__ == '__main__':
    unittest.main()