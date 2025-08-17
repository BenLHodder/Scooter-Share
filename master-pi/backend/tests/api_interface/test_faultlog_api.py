import unittest
from unittest.mock import patch
from api_interface.api_interface import APIInterface
from api_interface.faultlog_api import FaultLogAPI


class TestFaultLogAPI(unittest.TestCase):

    def setUp(self):
        """Set up the test case with a FaultLogAPI instance."""
        base_url = "http://localhost:8080"
        self.api = FaultLogAPI(base_url)

    @patch.object(APIInterface, "_send_get_request")
    def test_get_fault_by_id(self, mock_get):
        """Test the get_fault_by_id method."""
        mock_response = {
            "fault_id": 1,
            "scooter_id": 100,
            "description": "Flat tire",
            "status": "Open",
        }
        mock_get.return_value = mock_response

        fault_id = 1
        response = self.api.get_fault_by_id(fault_id)

        mock_get.assert_called_once_with(f"fault/{fault_id}")
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, "_send_get_request")
    def test_get_open_faults(self, mock_get):
        """Test the get_open_faults method."""
        mock_response = [
            {
                "fault_id": 1,
                "scooter_id": 100,
                "description": "Flat tire",
                "status": "Open",
            },
            {
                "fault_id": 2,
                "scooter_id": 101,
                "description": "Battery issue",
                "status": "Open",
            },
        ]
        mock_get.return_value = mock_response

        response = self.api.get_open_faults()

        mock_get.assert_called_once_with("fault/open_faults")
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, "_send_get_request")
    def test_get_fault_by_scooter(self, mock_get):
        """Test the get_fault_by_scooter method."""
        mock_response = {
            "fault_id": 1,
            "scooter_id": 100,
            "description": "Flat tire",
            "status": "Open",
        }
        mock_get.return_value = mock_response

        scooter_id = 100
        response = self.api.get_fault_by_scooter(scooter_id)

        mock_get.assert_called_once_with(f"fault/scooter/{scooter_id}")
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, "_send_put_request")
    def test_update_scooter_fault(self, mock_put):
        """Test the update_scooter_fault method."""
        mock_response = {"status": "success"}
        mock_put.return_value = mock_response

        fault_data = {"fault_id": 1, "description": "Flat tire", "status": "Open"}
        response = self.api.update_scooter_fault(fault_data)

        mock_put.assert_called_once_with("fault/update_scooter_fault", fault_data)
        self.assertEqual(response, mock_response)

    @patch.object(APIInterface, "_send_put_request")
    def test_resolve_scooter_fault(self, mock_put):
        """Test the resolve_scooter_fault method."""
        mock_response = {"status": "success"}
        mock_put.return_value = mock_response

        fault_id = 1
        resolution_data = {"resolved": True, "notes": "Tire replaced"}
        response = self.api.resolve_scooter_fault(fault_id, resolution_data)

        mock_put.assert_called_once_with(
            f"fault/resolve_scooter_fault/{fault_id}", resolution_data
        )
        self.assertEqual(response, mock_response)


if __name__ == "__main__":
    unittest.main()
