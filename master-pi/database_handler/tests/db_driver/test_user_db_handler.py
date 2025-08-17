import unittest
import re
from unittest.mock import MagicMock
from db_driver.user_db_handler import UserHandler

class TestUserHandler(unittest.TestCase):
    def setUp(self):
        # Set up a mock database driver and pass it to UserHandler
        self.mock_db_driver = MagicMock()
        self.user_handler = UserHandler(db_info='resources/database_info.json')
        self.user_handler._db_driver = self.mock_db_driver

    def assert_query_called_once_with(self, expected_query, *args, **kwargs):
        actual_query, actual_params = self.mock_db_driver.execute_query.call_args[0]
        
        # Normalize whitespace by removing all types of whitespace
        def normalize_whitespace(query):
            return re.sub(r'\s+', ' ', query.strip())

        normalized_expected_query = normalize_whitespace(expected_query)
        normalized_actual_query = normalize_whitespace(actual_query)
        
        self.assertEqual(normalized_expected_query, normalized_actual_query)
        self.assertEqual(args, actual_params)

    def test_register_customer_success(self):
        email = "test@example.com"
        password = "hashed_password"
        first_name = "John"
        last_name = "Doe"
        phone_no = "1234567890"
        funds = 100.0
        role = "Customer"
        
        # Call the method to test
        self.user_handler.register_customer(email, password, first_name, last_name, phone_no, funds, role)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "INSERT INTO SystemUser (email, password, firstName, lastName, phoneNo, funds, role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            email, password, first_name, last_name, phone_no, funds, role
        )
        
    def test_register_customer_already_exists(self):
        email = "test@example.com"
        password = "hashed_password"
        first_name = "John"
        last_name = "Doe"
        phone_no = "1234567890"
        funds = 100.0
        role = "Customer"
        
        # Configure the mock to raise an exception
        self.mock_db_driver.execute_query.side_effect = Exception("duplicate key value violates unique constraint \"customer_pkey\"")
        
        # Call the method to test
        response, status_code = self.user_handler.register_customer(email, password, first_name, last_name, phone_no, funds, role)
        
        # Verify the response
        self.assertEqual(response, {"error": "An unexpected error occurred."})
        self.assertEqual(status_code, 500)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "INSERT INTO SystemUser (email, password, firstName, lastName, phoneNo, funds, role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            email, password, first_name, last_name, phone_no, funds, role
        )
        
        # Ensure rollback was called
        self.mock_db_driver.connection.rollback.assert_called_once()
                
    def test_get_login_details_success(self):
        email = "test@example.com"
        password = "hashed_password"
        
        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [(email, password)]
        
        # Call the method to test
        result = self.user_handler.get_login_details(email)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT email, password FROM SystemUser WHERE email = %s",
            email
        )
        
        # Verify the result
        self.assertEqual(result, (email, password))

    def test_get_login_details_no_user(self):
        email = "nonexistent@example.com"
        
        # Set up the mock return value to simulate no result
        self.mock_db_driver.execute_query.return_value = []
        
        # Call the method to test
        result = self.user_handler.get_login_details(email)
        
        # Verify the result
        self.assertIsNone(result)

    def test_delete_customer_success(self):
        email = "test@example.com"
        
        # Call the method to test
        self.user_handler.delete_customer(email)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "DELETE FROM SystemUser WHERE email = %s",
            email
        )

    def test_update_customer_funds_success(self):
        email = "test@example.com"
        new_funds = 200.0
        
        # Call the method to test
        self.user_handler.update_customer_funds(email, new_funds)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE SystemUser SET funds = %s WHERE email = %s",
            new_funds, email
        )

    def test_get_customer_success(self):
        email = "test@example.com"
        customer_data = {
            'email': email,
            'password': 'hashed_password',
            'firstName': 'John',
            'lastName': 'Doe',
            'phoneNo': '1234567890',
            'funds': 100.0,
            'role': 'Customer'
        }
        
        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [(email, 'hashed_password', 'John', 'Doe', '1234567890', 100.0, 'Customer')]
        
        # Call the method to test
        result = self.user_handler.get_customer(email)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM SystemUser WHERE email = %s",
            email
        )
        
        # Verify the result
        self.assertEqual(result, customer_data)

    def test_get_customer_no_user(self):
        email = "nonexistent@example.com"
        
        # Set up the mock return value to simulate no result
        self.mock_db_driver.execute_query.return_value = []
        
        # Call the method to test
        result = self.user_handler.get_customer(email)
        
        # Verify the result
        self.assertIsNone(result)
        
    def test_get_all_customers_success(self):
        customers_data = [
            ('user1@example.com', 'hashed_password1', 'John', 'Doe', '1234567890', 100.0, 'Customer'),
            ('user2@example.com', 'hashed_password2', 'Jane', 'Doe', '0987654321', 50.0, 'Customer')
        ]

        expected_customers = [
            {
                'email': 'user1@example.com',
                'password': 'hashed_password1',
                'firstName': 'John',
                'lastName': 'Doe',
                'phoneNo': '1234567890',
                'funds': 100.0,
                'role': 'Customer'
            },
            {
                'email': 'user2@example.com',
                'password': 'hashed_password2',
                'firstName': 'Jane',
                'lastName': 'Doe',
                'phoneNo': '0987654321',
                'funds': 50.0,
                'role': 'Customer'
            }
        ]
        
        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = customers_data
        
        # Call the method to test
        result = self.user_handler.get_all_customers()
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM SystemUser WHERE role = %s",
            'Customer'
        )
        
        # Verify the result
        self.assertEqual(result, expected_customers)

    def test_get_all_customers_no_customers(self):
        # Set up the mock return value to simulate no customers
        self.mock_db_driver.execute_query.return_value = []
        
        # Call the method to test
        result = self.user_handler.get_all_customers()
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM SystemUser WHERE role = %s",
            'Customer'
        )
        
        # Verify the result
        self.assertEqual(result, [])

    def test_update_user_details_success(self):
        email = 'alice.smith@example.com'
        password = 'newpassword123'
        first_name = 'Alice'
        last_name = 'Smith'
        phone_no = '555-1234'
        funds = 50.0
        role = 'Customer'

        self.user_handler.update_user_details(email, password, first_name, last_name, phone_no, funds, role)

        self.assert_query_called_once_with(
            """
            UPDATE SystemUser
            SET password = %s, firstName = %s, lastName = %s, phoneNo = %s, funds = %s, role = %s
            WHERE email = %s
            """,
            password, first_name, last_name, phone_no, funds, role, email
        )
        
    def test_get_engineer_emails_success(self):
        engineers_data = [
            ('engineer1@example.com',),
            ('engineer2@example.com',)
        ]

        expected_emails = ['engineer1@example.com', 'engineer2@example.com']
        
        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = engineers_data
        
        # Call the method to test
        result = self.user_handler.get_engineer_emails()
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT email FROM SystemUser WHERE role = %s",
            'Engineer'
        )
        
        # Verify the result
        self.assertEqual(result, expected_emails)

    def test_get_engineer_emails_no_engineers(self):
        # Set up the mock return value to simulate no engineers
        self.mock_db_driver.execute_query.return_value = []
        
        # Call the method to test
        result = self.user_handler.get_engineer_emails()
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT email FROM SystemUser WHERE role = %s",
            'Engineer'
        )
        
        # Verify the result
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
