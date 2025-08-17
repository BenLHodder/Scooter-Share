import unittest
from unittest.mock import patch
from api_interface.api_interface import APIInterface
from api_interface.scooter_api import ScooterAPI

class TestScooterAPI(unittest.TestCase):

    def setUp(self):
        """Set up the test case with a ScooterAPI instance."""
        base_url = "http://localhost:8080"
        self.api = ScooterAPI(base_url)

    @patch.object(APIInterface, '_send_get_request')
    def test_get_scooter(self, mock_get):
        # Arrange
        scooter_id = 456
        expected_endpoint = f"scooter/{scooter_id}"
        mock_get.return_value = {"scooterID": scooter_id, "status": "available"}

        # Act
        response = self.api.get_scooter(scooter_id)

        # Assert
        mock_get.assert_called_once_with(expected_endpoint)
        self.assertEqual(response['scooterID'], scooter_id)
        self.assertEqual(response['status'], "available")

    @patch.object(APIInterface, '_send_put_request')
    def test_update_scooter_status(self, mock_put):
        # Arrange
        scooter_data = {"scooterID": 456, "status": "in-use"}
        expected_endpoint = "scooter/update_scooter_status"
        mock_put.return_value = {"status": "updated"}

        # Act
        response = self.api.update_scooter_status(scooter_data)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint, scooter_data)
        self.assertEqual(response['status'], "updated")

    @patch.object(APIInterface, '_send_get_request')
    def test_get_all_scooters(self, mock_get):
        # Arrange
        expected_endpoint = "scooter/scooters"
        mock_get.return_value = [
            {
                "scooterID": 1,
                "make": "ScooterBrand",
                "colour": "Red",
                "longitude": 12.34,
                "latitude": 56.78,
                "costMin": 0.25,
                "batteryPercentage": 75.0,
                "status": "available",
                "ipAddress": "192.168.1.1",
                "faultNotes": ""
            },
            # Add more scooter entries if needed
        ]

        # Act
        response = self.api.get_all_scooters()

        # Assert
        mock_get.assert_called_once_with(expected_endpoint)
        self.assertTrue(isinstance(response, list))
        self.assertGreater(len(response), 0)  # Ensure there's at least one scooter in the list
        self.assertEqual(response[0]['scooterID'], 1)
        self.assertEqual(response[0]['make'], "ScooterBrand")
        self.assertEqual(response[0]['colour'], "Red")
        
    @patch.object(APIInterface, '_send_put_request')
    def test_update_scooter_location(self, mock_put):
        # Arrange
        scooter_id = 456
        scooter_data = {"latitude": 50.1234, "longitude": -0.5678}
        expected_endpoint = f"scooter/update_location/{scooter_id}"
        mock_put.return_value = {"message": "Scooter location updated successfully."}

        # Act
        response = self.api.update_scooter_location(scooter_id, scooter_data)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint, scooter_data)
        self.assertEqual(response['message'], "Scooter location updated successfully.")

    @patch.object(APIInterface, '_send_put_request')
    def test_update_scooter_ip_address(self, mock_put):
        # Arrange
        scooter_id = 456
        scooter_data = {"ip_address": "192.168.1.20"}
        expected_endpoint = f"scooter/update_ip_address/{scooter_id}"
        mock_put.return_value = {"message": "Scooter IP address updated successfully."}

        # Act
        response = self.api.update_scooter_ip_address(scooter_id, scooter_data)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint, scooter_data)
        self.assertEqual(response['message'], "Scooter IP address updated successfully.")

if __name__ == '__main__':
    unittest.main()
