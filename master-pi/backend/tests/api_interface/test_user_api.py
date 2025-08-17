import unittest
from unittest.mock import patch
from api_interface.api_interface import APIInterface
from api_interface.user_api import UserAPI

class TestCustomerAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up the test case with a UserAPI instance."""
        base_url = "http://localhost:8080"
        self.api = UserAPI(base_url)
    
    @patch.object(APIInterface, '_send_get_request')
    def test_get_customer(self, mock_get):
        """Test the get_customer method."""
        mock_response = {'email': 'alice.smith@example.com', 'name': 'Alice Smith', 'phone': '555-1234', 'funds': 150.50, 'role': 'Customer'}
        mock_get.return_value = mock_response

        email = 'alice.smith@example.com'
        response = self.api.get_customer(email)
        
        mock_get.assert_called_once_with(f"user/{email}")
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, '_send_get_request')
    def test_get_customer_login(self, mock_get):
        """Test the get_customer_login method."""
        mock_response = {'email': 'alice.smith@example.com', 'password': 'password123'}
        mock_get.return_value = mock_response

        email = 'alice.smith@example.com'
        response = self.api.get_customer_login(email)

        mock_get.assert_called_once_with(f"user/login/{email}")
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, '_send_post_request')
    def test_register_customer(self, mock_post):
        """Test the register_customer method."""
        mock_response = {'status': 'success'}
        mock_post.return_value = mock_response

        customer_data = {
            'email': 'alice.smith@example.com',
            'password': 'password123',
            'firstName': 'Alice',
            'lastName': 'Smith',
            'phoneNo': '555-1234',
            'funds': 150.50,
            'role': 'Customer'
        }
        response = self.api.register_customer(customer_data)

        mock_post.assert_called_once_with("user/register", customer_data)
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, '_send_delete_request')
    def test_delete_customer(self, mock_delete):
        """Test the delete_customer method."""
        mock_response = {'status': 'success'}
        mock_delete.return_value = mock_response

        email = 'alice.smith@example.com'
        response = self.api.delete_customer(email)

        mock_delete.assert_called_once_with(f"user/delete/{email}")
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, '_send_put_request')
    def test_update_funds(self, mock_put):
        """Test the update_funds method."""
        mock_response = {'status': 'success'}
        mock_put.return_value = mock_response

        update_data = {
            'email': 'alice.smith@example.com',
            'funds': 200.00
        }
        response = self.api.update_funds(update_data)

        mock_put.assert_called_once_with("user/update_funds", update_data)
        self.assertEqual(response, mock_response)
        
    @patch.object(APIInterface, '_send_get_request')
    def test_get_all_customers(self, mock_get):
        """Test the get_all_customers method."""
        mock_response = [
            {'email': 'alice.smith@example.com', 'name': 'Alice Smith', 'phone': '555-1234', 'funds': 150.50, 'role': 'Customer'},
            {'email': 'bob.jones@example.com', 'name': 'Bob Jones', 'phone': '555-9876', 'funds': 200.00, 'role': 'Customer'}
        ]
        mock_get.return_value = mock_response

        response = self.api.get_all_customers()

        mock_get.assert_called_once_with("user/customers")
        self.assertEqual(response, mock_response)
        
    @patch.object(APIInterface, '_send_get_request')
    def test_get_all_engineer_emails(self, mock_get):
        """Test the get_all_engineer_emails method."""
        mock_response = ["engineer1@example.com", "engineer2@example.com"]
        mock_get.return_value = mock_response

        response = self.api.get_all_engineer_emails()

        mock_get.assert_called_once_with("user/engineers/emails")
        self.assertEqual(response, mock_response)

if __name__ == '__main__':
    unittest.main()
