import unittest
import re
from unittest.mock import MagicMock
from db_driver.scooter_db_handler import ScooterHandler  # Adjust the import according to your module structure

class TestScooterHandler(unittest.TestCase):
    def setUp(self):
        # Set up a mock database driver and pass it to ScooterHandler
        self.mock_db_driver = MagicMock()
        self.scooter_handler = ScooterHandler(db_info='resources/database_info.json')
        self.scooter_handler._db_driver = self.mock_db_driver

    def assert_query_called_once_with(self, expected_query, *args):
        call_args = self.mock_db_driver.execute_query.call_args[0]
        actual_query = call_args[0]
        
        # If there are no parameters, actual_params will be an empty tuple
        actual_params = call_args[1] if len(call_args) > 1 else ()

        # Normalize whitespace by removing all types of whitespace
        def normalize_whitespace(query):
            return re.sub(r'\s+', ' ', query.strip())

        normalized_expected_query = normalize_whitespace(expected_query)
        normalized_actual_query = normalize_whitespace(actual_query)

        self.assertEqual(normalized_expected_query, normalized_actual_query)
        self.assertEqual(args, actual_params)

    def test_update_scooter_status_success(self):
        scooter_id = 1
        new_status = 'available'
        
        # Call the method to test
        self.scooter_handler.update_scooter_status(scooter_id, new_status)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Scooter SET status = %s WHERE scooterID = %s",
            new_status, scooter_id
        )

    def test_get_scooter_success(self):
        scooter_id = 1
        scooter_data = {
            'scooterID': 1,
            'make': 'Make',
            'colour': 'Colour',
            "longitude": 50.1234,
            "latitude": -0.5678,
            'costMin': 10.0,
            'batteryPercentage': 100,
            'status': 'available',
            "ipAddress": "192.168.1.10"
        }

        # Mock the return value of execute_query
        self.mock_db_driver.execute_query.return_value = [(1, 'Make', 'Colour', 50.1234, -0.5678, 10.0, 100, 'available', '192.168.1.10')]
        
        # Call the method to test
        result = self.scooter_handler.get_scooter(scooter_id)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Scooter WHERE scooterID = %s",
            scooter_id
        )
        
        # Verify the result
        self.assertEqual(result, scooter_data)

    def test_get_scooter_not_found(self):
        scooter_id = 999
        
        # Mock the return value to simulate no result
        self.mock_db_driver.execute_query.return_value = []
        
        # Call the method to test
        result = self.scooter_handler.get_scooter(scooter_id)
        
        # Verify the result
        self.assertIsNone(result)

    def test_get_all_scooters_success(self):
        scooter_data_list = [
            {
                'scooterID': 1,
                'make': 'Make1',
                'colour': 'Colour1',
                "longitude": 50.1234,
                "latitude": -0.5678,
                'costMin': 10.0,
                'batteryPercentage': 100,
                'status': 'available',
                "ipAddress": "192.168.1.10"
            },
            {
                'scooterID': 2,
                'make': 'Make2',
                'colour': 'Colour2',
                "longitude": 51.1234,
                "latitude": -1.5678,
                'costMin': 15.0,
                'batteryPercentage': 80,
                'status': 'in use',
                "ipAddress": "192.168.1.11"
            }
        ]

        # Mock the return value of execute_query
        self.mock_db_driver.execute_query.return_value = [
            (1, 'Make1', 'Colour1', 50.1234, -0.5678, 10.0, 100, 'available', '192.168.1.10'),
            (2, 'Make2', 'Colour2', 51.1234, -1.5678, 15.0, 80, 'in use', '192.168.1.11')
        ]
        
        # Call the method to test
        result = self.scooter_handler.get_all_scooters()
        
        # Check that execute_query was called with the expected query and no parameters
        self.assert_query_called_once_with("SELECT * FROM Scooter")
        
        # Verify the result
        self.assertEqual(result, scooter_data_list)
        
    def test_update_scooter_location_success(self):
        scooter_id = 1
        latitude = 50.1234
        longitude = -0.5678

        # Call the method to test
        self.scooter_handler.update_scooter_location(scooter_id, latitude, longitude)

        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Scooter SET latitude = %s, longitude = %s WHERE scooterID = %s",
            latitude, longitude, scooter_id
        )

    def test_update_scooter_ip_address_success(self):
        scooter_id = 1
        new_ip_address = "192.168.1.20"

        # Call the method to test
        self.scooter_handler.update_scooter_ip_address(scooter_id, new_ip_address)

        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Scooter SET ipAddress = %s WHERE scooterID = %s",
            new_ip_address, scooter_id
        )
        
    def test_update_scooter_details_success(self):
        scooter_id = 1
        make = 'BrandX'
        colour = 'Red'
        latitude = 51.5074
        longitude = -0.1278
        cost_min = 0.15
        battery_percentage = 90
        status = 'available'
        ip_address = '192.168.1.100'

        self.scooter_handler.update_scooter_details(
            scooter_id, make, colour, latitude, longitude, cost_min,
            battery_percentage, status, ip_address
        )

        self.assert_query_called_once_with(
            """
            UPDATE Scooter
            SET make = %s, colour = %s, latitude = %s, longitude = %s, costMin = %s,
                batteryPercentage = %s, status = %s, ipAddress = %s
            WHERE scooterID = %s
            """,
            make, colour, latitude, longitude, cost_min, battery_percentage, status, ip_address, scooter_id
        )

if __name__ == '__main__':
    unittest.main()
