import unittest
import re
import pytz
from datetime import datetime
from unittest.mock import MagicMock
from db_driver.booking_db_handler import BookingHandler

class TestBookingHandler(unittest.TestCase):
    def setUp(self):
        # Set up a mock database driver and pass it to BookingHandler
        self.mock_db_driver = MagicMock()
        self.booking_handler = BookingHandler(db_info='resources/database_info.json')
        self.booking_handler._db_driver = self.mock_db_driver

    def assert_query_called_once_with(self, expected_query, *args):
        actual_query, actual_params = self.mock_db_driver.execute_query.call_args[0]

        # Normalize whitespace by removing all types of whitespace
        def normalize_whitespace(query):
            return re.sub(r'\s+', ' ', query.strip())

        normalized_expected_query = normalize_whitespace(expected_query)
        normalized_actual_query = normalize_whitespace(actual_query)

        self.assertEqual(normalized_expected_query, normalized_actual_query)
        self.assertEqual(args, actual_params)

    def test_add_booking_success(self):
        # Test data
        email = "test@example.com"
        scooter_id = 1
        start_datetime = datetime(2024, 9, 15, 10, 0, tzinfo=pytz.timezone('Australia/Sydney'))
        end_datetime = datetime(2024, 9, 15, 12, 0, tzinfo=pytz.timezone('Australia/Sydney'))
        cost = 50.0
        deposit_cost = 10.0
        status = 'Active'
        expected_booking_id = 42  # Assume the returned booking ID will be 42

        # Mock the database driver's execute_query method to return the booking ID
        self.booking_handler._db_driver.execute_query.return_value = expected_booking_id

        # Call the method to test
        booking_id = self.booking_handler.add_booking(email, scooter_id, start_datetime, end_datetime, cost, deposit_cost, status)

        # The expected SQL query
        expected_query = """
            INSERT INTO Booking (email, scooterID, startDateTime, endDateTime, cost, depositCost, googleID, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING bookingID
            """

        # Assert that execute_query was called with the correct SQL query and parameters
        self.assert_query_called_once_with(
            expected_query,
            email, scooter_id, start_datetime, end_datetime, cost, deposit_cost, None, status
        )

        # Assert that the returned booking ID matches the expected value
        self.assertEqual(booking_id, expected_booking_id)

    def test_cancel_booking_success(self):
        booking_id = 123
        
        # Call the method to test
        self.booking_handler.cancel_booking(booking_id)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Booking SET status = 'Cancelled' WHERE bookingID = %s",
            booking_id
        )

    def test_start_booking_success(self):
        booking_id = 123
        actual_start_datetime = datetime(2024, 9, 15, 10, 5, tzinfo=pytz.timezone('Australia/Sydney'))
        
        # Call the method to test
        self.booking_handler.start_booking(booking_id, actual_start_datetime)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Booking SET actualStartDateTime = %s WHERE bookingID = %s",
            actual_start_datetime, booking_id
        )

    def test_end_booking_success(self):
        booking_id = 123
        actual_end_datetime = datetime(2024, 9, 15, 11, 50, tzinfo=pytz.timezone('Australia/Sydney'))
        
        # Call the method to test
        self.booking_handler.end_booking(booking_id, actual_end_datetime)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Booking SET actualEndDateTime = %s WHERE bookingID = %s",
            actual_end_datetime, booking_id
        )

    def test_get_booking_success(self):
        booking_id = 123
        booking_data = {
            'email': 'test@example.com',
            'scooterID': 1,
            'bookingID': 123,
            'startDateTime': '2024-09-15 10:00:00',
            'endDateTime': '2024-09-15 12:00:00',
            'actualStartDateTime': '2024-09-15 10:05:00',
            'actualEndDateTime': '2024-09-15 11:50:00',
            'cost': 50.0,
            'depositCost': 10.0,
            'googleID': None,
            'status': 'Active'
        }

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [
            ('test@example.com', 1, 123, '2024-09-15 10:00:00', '2024-09-15 12:00:00',
            '2024-09-15 10:05:00', '2024-09-15 11:50:00', 50.0, 10.0, None, 'Active')  # googleID set to None
        ]

        # Call the method to test
        result = self.booking_handler.get_booking(booking_id)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Booking WHERE bookingID = %s",
            booking_id
        )

        # Verify the result
        self.assertEqual(result, booking_data)

    def test_get_booking_no_result(self):
        booking_id = 999
        
        # Set up the mock return value to simulate no result
        self.mock_db_driver.execute_query.return_value = []

        # Call the method to test
        result = self.booking_handler.get_booking(booking_id)

        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Booking WHERE bookingID = %s",
            booking_id
        )

        # Verify that no result was found
        self.assertIsNone(result)

    def test_get_all_bookings_for_customer_success(self):
        email = "test@example.com"
        bookings = [
            {'email': 'test@example.com', 'scooterID': 1, 'bookingID': 123, 'startDateTime': '2024-09-15 10:00:00', 
            'endDateTime': '2024-09-15 12:00:00', 'actualStartDateTime': '2024-09-15 10:05:00', 
            'actualEndDateTime': '2024-09-15 11:50:00', 'cost': 50.0, 'depositCost': 10.0, 'googleID': None, 'status': 'Active'},
            {'email': 'test@example.com', 'scooterID': 2, 'bookingID': 124, 'startDateTime': '2024-09-16 09:00:00', 
            'endDateTime': '2024-09-16 11:00:00', 'actualStartDateTime': '2024-09-16 09:10:00', 
            'actualEndDateTime': '2024-09-16 10:50:00', 'cost': 60.0, 'depositCost': 15.0, 'googleID': None, 'status': 'Active'}
        ]

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [
            ('test@example.com', 1, 123, '2024-09-15 10:00:00', '2024-09-15 12:00:00', '2024-09-15 10:05:00', 
            '2024-09-15 11:50:00', 50.0, 10.0, None, 'Active'),
            ('test@example.com', 2, 124, '2024-09-16 09:00:00', '2024-09-16 11:00:00', '2024-09-16 09:10:00', 
            '2024-09-16 10:50:00', 60.0, 15.0, None, 'Active')
        ]

        # Call the method to test
        result = self.booking_handler.get_all_bookings_for_customer(email)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Booking WHERE email = %s ORDER BY startDateTime DESC",
            email
        )

        # Verify the result
        self.assertEqual(result, bookings)

    def test_get_all_booked_scooters_and_times_success(self):
        booked_scooters = [
            {'scooterID': 1, 'startDateTime': '2024-09-15 10:00:00', 'endDateTime': '2024-09-15 12:00:00', 'status': 'Complete'},
            {'scooterID': 2, 'startDateTime': '2024-09-16 09:00:00', 'endDateTime': '2024-09-16 11:00:00', 'status': 'Complete'}
        ]

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [
            (1, '2024-09-15 10:00:00', '2024-09-15 12:00:00', 'Complete'),
            (2, '2024-09-16 09:00:00', '2024-09-16 11:00:00', 'Complete')
        ]

        # Call the method to test
        result = self.booking_handler.get_all_booked_scooters_and_times()
        
        # Check that execute_query was called with the expected query
        self.mock_db_driver.execute_query.assert_called_once_with(
            "SELECT scooterID, startDateTime, endDateTime, status FROM Booking"
        )

        # Verify the result
        self.assertEqual(result, booked_scooters)
        
    def test_set_booking_complete_success(self):
        booking_id = 123
        
        # Call the method to test
        self.booking_handler.set_booking_complete(booking_id)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Booking SET status = 'Complete' WHERE bookingID = %s",
            booking_id
        )
        
    def test_update_booking_cost_success(self):
        booking_id = 123
        new_cost = 75.0

        # Call the method to test
        self.booking_handler.update_booking_cost(booking_id, new_cost)

        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Booking SET cost = %s WHERE bookingID = %s",
            new_cost, booking_id
        )

    def test_get_all_active_bookings_success(self):
        active_bookings = [
            {'email': 'test@example.com', 'scooterID': 1, 'bookingID': 123, 'startDateTime': '2024-09-15 10:00:00', 
            'endDateTime': '2024-09-15 12:00:00', 'actualStartDateTime': '2024-09-15 10:05:00', 
            'actualEndDateTime': '2024-09-15 11:50:00', 'cost': 50.0, 'depositCost': 10.0, 
            'googleID': None,
            'status': 'Active'},
            {'email': 'user2@example.com', 'scooterID': 2, 'bookingID': 124, 'startDateTime': '2024-09-16 09:00:00', 
            'endDateTime': '2024-09-16 11:00:00', 'actualStartDateTime': '2024-09-16 09:10:00', 
            'actualEndDateTime': '2024-09-16 10:50:00', 'cost': 60.0, 'depositCost': 15.0, 
            'googleID': None,
            'status': 'Active'}
        ]
        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [
            ('test@example.com', 1, 123, '2024-09-15 10:00:00', '2024-09-15 12:00:00', '2024-09-15 10:05:00', 
            '2024-09-15 11:50:00', 50.0, 10.0, None, 'Active'),
            ('user2@example.com', 2, 124, '2024-09-16 09:00:00', '2024-09-16 11:00:00', '2024-09-16 09:10:00', 
            '2024-09-16 10:50:00', 60.0, 15.0, None, 'Active')
        ]

        # Call the method to test
        result = self.booking_handler.get_all_active_bookings()
        
        # Check that execute_query was called with the expected query
        self.mock_db_driver.execute_query.assert_called_once_with(
            "SELECT * FROM Booking WHERE status = 'Active'"
        )

        # Verify the result
        self.assertEqual(result, active_bookings)
        
    def test_set_booking_googleID_success(self):
        booking_id = 123
        google_id = "abc123-google"

        # Call the method to test
        self.booking_handler.set_booking_googleID(booking_id, google_id)

        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "UPDATE Booking SET googleID = %s WHERE bookingID = %s",
            google_id, booking_id
        )

    def test_get_all_bookings_for_scooter_success(self):
        scooter_id = 1
        bookings = [
            {'email': 'test@example.com', 'scooterID': 1, 'bookingID': 123, 'startDateTime': '2024-09-15 10:00:00', 
            'endDateTime': '2024-09-15 12:00:00', 'actualStartDateTime': '2024-09-15 10:05:00', 
            'actualEndDateTime': '2024-09-15 11:50:00', 'cost': 50.0, 'depositCost': 10.0, 'googleID': None, 'status': 'Active'},
            {'email': 'user2@example.com', 'scooterID': 1, 'bookingID': 124, 'startDateTime': '2024-09-16 09:00:00', 
            'endDateTime': '2024-09-16 11:00:00', 'actualStartDateTime': '2024-09-16 09:10:00', 
            'actualEndDateTime': '2024-09-16 10:50:00', 'cost': 60.0, 'depositCost': 15.0, 'googleID': None, 'status': 'Active'}
        ]

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = [
            ('test@example.com', 1, 123, '2024-09-15 10:00:00', '2024-09-15 12:00:00', '2024-09-15 10:05:00', 
            '2024-09-15 11:50:00', 50.0, 10.0, None, 'Active'),
            ('user2@example.com', 1, 124, '2024-09-16 09:00:00', '2024-09-16 11:00:00', '2024-09-16 09:10:00', 
            '2024-09-16 10:50:00', 60.0, 15.0, None, 'Active')
        ]

        # Call the method to test
        result = self.booking_handler.get_all_bookings_for_scooter(scooter_id)
        
        # Check that execute_query was called with the expected query and parameters
        self.assert_query_called_once_with(
            "SELECT * FROM Booking WHERE scooterID = %s ORDER BY startDateTime DESC",
            scooter_id
        )

        # Verify the result
        self.assertEqual(result, bookings)

if __name__ == '__main__':
    unittest.main()
