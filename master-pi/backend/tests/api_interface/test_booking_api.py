import unittest
from unittest.mock import patch
from api_interface.api_interface import APIInterface
from api_interface.booking_api import BookingAPI

class TestBookingAPI(unittest.TestCase):

    def setUp(self):
        """Set up the test case with a BookingAPI instance."""
        base_url = "http://localhost:8080"
        self.api = BookingAPI(base_url)

    @patch.object(APIInterface, '_send_get_request')
    def test_get_booking(self, mock_get):
        # Arrange
        booking_id = 123
        expected_endpoint = f"booking/{booking_id}"
        mock_get.return_value = {"bookingID": booking_id, "status": "Active"}

        # Act
        response = self.api.get_booking(booking_id)

        # Assert
        mock_get.assert_called_once_with(expected_endpoint)
        self.assertEqual(response['bookingID'], booking_id)
        self.assertEqual(response['status'], "Active")

    @patch.object(APIInterface, '_send_post_request')
    def test_add_booking(self, mock_post):
        # Arrange
        booking_data = {"email": "test@example.com", "scooterID": 1, "cost": 10.0}
        expected_endpoint = "booking/add_booking"
        mock_post.return_value = {"status": "success"}

        # Act
        response = self.api.add_booking(booking_data)

        # Assert
        mock_post.assert_called_once_with(expected_endpoint, booking_data)
        self.assertEqual(response['status'], "success")

    @patch.object(APIInterface, '_send_delete_request')
    def test_cancel_booking(self, mock_delete):
        # Arrange
        booking_id = 123
        expected_endpoint = f"booking/cancel_booking/{booking_id}"
        mock_delete.return_value = {"status": "cancelled"}

        # Act
        response = self.api.cancel_booking(booking_id)

        # Assert
        mock_delete.assert_called_once_with(expected_endpoint)
        self.assertEqual(response['status'], "cancelled")

    @patch.object(APIInterface, '_send_put_request')
    def test_start_booking(self, mock_put):
        # Arrange
        booking_data = {"bookingID": 123, "startTime": "2024-09-01 10:00:00"}
        expected_endpoint = "booking/start_booking"
        mock_put.return_value = {"status": "started"}

        # Act
        response = self.api.start_booking(booking_data)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint, booking_data)
        self.assertEqual(response['status'], "started")

    @patch.object(APIInterface, '_send_put_request')
    def test_end_booking(self, mock_put):
        # Arrange
        booking_data = {"bookingID": 123, "endTime": "2024-09-01 10:30:00"}
        expected_endpoint = "booking/end_booking"
        mock_put.return_value = {"status": "ended"}

        # Act
        response = self.api.end_booking(booking_data)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint, booking_data)
        self.assertEqual(response['status'], "ended")

    @patch.object(APIInterface, '_send_put_request')
    def test_update_booking_status_complete(self, mock_put):
        # Arrange
        booking_id = 123
        expected_endpoint = f"booking/complete/{booking_id}"
        mock_put.return_value = {"status": "completed"}

        # Act
        response = self.api.update_booking_status_complete(booking_id)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint)
        self.assertEqual(response['status'], "completed")

    @patch.object(APIInterface, '_send_put_request')
    def test_update_booking_cost(self, mock_put):
        # Arrange
        booking_id = 123
        booking_data = {"cost": 15.0}
        expected_endpoint = f"booking/update_cost/{booking_id}"
        mock_put.return_value = {"message": "Booking cost updated successfully."}

        # Act
        response = self.api.update_booking_cost(booking_id, booking_data)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint, booking_data)
        self.assertEqual(response['message'], "Booking cost updated successfully.")

    @patch.object(APIInterface, '_send_get_request')
    def test_get_all_active_bookings(self, mock_get):
        # Arrange
        expected_endpoint = "booking/active"
        mock_get.return_value = [
            {"bookingID": 123, "status": "Active"},
            {"bookingID": 124, "status": "Active"}
        ]

        # Act
        response = self.api.get_all_active_bookings()

        # Assert
        mock_get.assert_called_once_with(expected_endpoint)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]['bookingID'], 123)
        self.assertEqual(response[1]['bookingID'], 124)
        self.assertEqual(response[0]['status'], "Active")
        self.assertEqual(response[1]['status'], "Active")

    @patch.object(APIInterface, '_send_put_request')
    def test_set_booking_googleid(self, mock_put):
        # Arrange
        booking_id = 123
        google_id = "some-google-id"
        expected_endpoint = f"booking/{booking_id}/set_googleID"
        mock_put.return_value = {"status": "Google ID set"}

        # Act
        response = self.api.set_booking_googleID(booking_id, google_id)

        # Assert
        mock_put.assert_called_once_with(expected_endpoint, google_id)
        self.assertEqual(response['status'], "Google ID set")

if __name__ == '__main__':
    unittest.main()
