import unittest
import re
import pytz
from datetime import datetime
from unittest.mock import MagicMock
from db_driver.transaction_db_handler import TransactionHandler

class TestTransactionHandler(unittest.TestCase):
    def setUp(self):
        # Set up a mock database driver and pass it to TransactionHandler
        self.mock_db_driver = MagicMock()
        self.transaction_handler = TransactionHandler(db_info='resources/database_info.json')
        self.transaction_handler._db_driver = self.mock_db_driver

    def assert_query_called_once_with(self, expected_query, *args, **kwargs):
        actual_query, actual_params = self.mock_db_driver.execute_query.call_args[0]

        # Normalize whitespace by removing all types of whitespace
        def normalize_whitespace(query):
            return re.sub(r'\s+', ' ', query.strip())

        normalized_expected_query = normalize_whitespace(expected_query)
        normalized_actual_query = normalize_whitespace(actual_query)

        self.assertEqual(normalized_expected_query, normalized_actual_query)
        self.assertEqual(args, actual_params)

    def test_add_transaction_success(self):
        email = "test@example.com"
        transaction_amount = 150.75
        transaction_datetime = datetime(2024, 9, 14, 15, 45, tzinfo=pytz.timezone('Australia/Sydney'))
        
        # Call the method to test
        self.transaction_handler.add_transaction(email, transaction_amount, transaction_datetime)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "INSERT INTO Transaction (email, datetime, transactionAmount) VALUES (%s, %s, %s)",
            email, transaction_datetime, transaction_amount
        )

    def test_get_transaction_success(self):
        transaction_id = 123
        transaction_data = {
            'email': 'test@example.com',
            'transactionID': 123,
            'datetime': '2024-09-14 15:45:00',
            'transactionAmount': 150.75
        }

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [
            ('test@example.com', 123, '2024-09-14 15:45:00', 150.75)
        ]

        # Call the method to test
        result = self.transaction_handler.get_transaction(transaction_id)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Transaction WHERE transactionID = %s",
            transaction_id
        )

        # Verify the result
        self.assertEqual(result, transaction_data)

    def test_get_transaction_no_result(self):
        transaction_id = 999

        # Set up the mock return value to simulate no result
        self.mock_db_driver.execute_query.return_value = []

        # Call the method to test
        result = self.transaction_handler.get_transaction(transaction_id)

        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Transaction WHERE transactionID = %s",
            transaction_id
        )

        # Verify that no result was found
        self.assertIsNone(result)
        
    def test_get_all_transactions_for_customer_success(self):
        email = "test@example.com"
        transactions_data = [
            {
                'email': 'test@example.com',
                'transactionID': 123,
                'datetime': '2024-09-14 15:45:00',
                'transactionAmount': 150.75
            },
            {
                'email': 'test@example.com',
                'transactionID': 124,
                'datetime': '2024-09-15 16:00:00',
                'transactionAmount': 200.00
            }
        ]

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [
            ('test@example.com', 123, '2024-09-14 15:45:00', 150.75),
            ('test@example.com', 124, '2024-09-15 16:00:00', 200.00)
        ]

        # Call the method to test
        result = self.transaction_handler.get_all_transactions_for_customer(email)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Transaction WHERE email = %s",
            email
        )

        # Verify the result
        self.assertEqual(result, transactions_data)

    def test_get_all_transactions_for_customer_no_result(self):
        email = "test@example.com"

        # Set up the mock return value to simulate no transactions
        self.mock_db_driver.execute_query.return_value = []

        # Call the method to test
        result = self.transaction_handler.get_all_transactions_for_customer(email)

        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Transaction WHERE email = %s",
            email
        )

        # Verify that no transactions were found
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
