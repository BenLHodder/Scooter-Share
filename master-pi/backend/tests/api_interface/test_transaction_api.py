import unittest
from unittest.mock import patch
from api_interface.api_interface import APIInterface
from api_interface.transaction_api import TransactionAPI

class TestTransactionAPI(unittest.TestCase):

    def setUp(self):
        """Set up the test case with a TransactionAPI instance."""
        base_url = "http://localhost:8080"
        self.api = TransactionAPI(base_url)

    @patch.object(APIInterface, '_send_get_request')
    def test_get_transaction(self, mock_get):
        # Arrange
        transaction_id = 789
        expected_endpoint = f"transaction/{transaction_id}"
        mock_get.return_value = {"transactionID": transaction_id, "status": "completed"}

        # Act
        response = self.api.get_transaction(transaction_id)

        # Assert
        mock_get.assert_called_once_with(expected_endpoint)
        self.assertEqual(response['transactionID'], transaction_id)
        self.assertEqual(response['status'], "completed")

    @patch.object(APIInterface, '_send_post_request')
    def test_add_transaction(self, mock_post):
        # Arrange
        transaction_data = {"customerID": 123, "amount": 25.50, "scooterID": 456}
        expected_endpoint = "transaction/add_transaction"
        mock_post.return_value = {"status": "success"}

        # Act
        response = self.api.add_transaction(transaction_data)

        # Assert
        mock_post.assert_called_once_with(expected_endpoint, transaction_data)
        self.assertEqual(response['status'], "success")

    @patch.object(APIInterface, '_send_get_request')
    def test_get_customer_transactions(self, mock_get):
        # Arrange
        customer_id = 123
        expected_endpoint = f"transaction/get_transactions/{customer_id}"
        mock_get.return_value = [
            {"transactionID": 1, "amount": 25.50, "status": "completed"},
            {"transactionID": 2, "amount": 15.75, "status": "pending"}
        ]

        # Act
        response = self.api.get_customer_transactions(customer_id)

        # Assert
        mock_get.assert_called_once_with(expected_endpoint)
        self.assertTrue(isinstance(response, list))
        self.assertGreater(len(response), 0)  # Ensure there's at least one transaction in the list
        self.assertEqual(response[0]['transactionID'], 1)
        self.assertEqual(response[0]['amount'], 25.50)
        self.assertEqual(response[0]['status'], "completed")

if __name__ == '__main__':
    unittest.main()
