import unittest
from unittest.mock import MagicMock
import re
from db_driver.faultlog_db_handler import FaultLogHandler


class TestFaultLogHandler(unittest.TestCase):
    def setUp(self):
        # Set up a mock database driver and pass it to FaultLogHandler
        self.mock_db_driver = MagicMock()
        self.fault_log_handler = FaultLogHandler(db_info="resources/database_info.json")
        self.fault_log_handler._db_driver = self.mock_db_driver

    def normalize_whitespace(self, query):
        """Helper method to normalize whitespace in SQL queries."""
        return re.sub(r"\s+", " ", query.strip())

    def test_update_scooter_fault_update_existing(self):
        scooter_id = 1
        fault_notes = "New fault notes"

        # Mock the result of checking for an open fault (returns an open fault)
        self.mock_db_driver.execute_query.return_value = [
            (1,)
        ]  # Represents faultID = 1

        # Call the method to test
        self.fault_log_handler.update_scooter_fault(scooter_id, fault_notes)

        # Check that execute_query was called with the expected update query
        expected_update_query = """
            UPDATE FaultLog
            SET faultNotes = %s
            WHERE faultID = %s;
        """
        self.assertEqual(
            self.normalize_whitespace(expected_update_query),
            self.normalize_whitespace(
                self.mock_db_driver.execute_query.call_args[0][0]
            ),
        )
        self.assertEqual(
            self.mock_db_driver.execute_query.call_args[0][1], (fault_notes, 1)
        )

    def test_update_scooter_fault_insert_new(self):
        scooter_id = 1
        fault_notes = "New fault notes"

        # Mock the result of checking for an open fault (returns no open fault)
        self.mock_db_driver.execute_query.return_value = []  # No open faults

        # Call the method to test
        self.fault_log_handler.update_scooter_fault(scooter_id, fault_notes)

        # Check that execute_query was called with the expected insert query
        expected_insert_query = """
            INSERT INTO FaultLog (scooterID, startDateTime, status, faultNotes, resolution)
            VALUES (%s, %s, 'Open', %s, NULL);
        """
        self.assertEqual(
            self.normalize_whitespace(expected_insert_query),
            self.normalize_whitespace(
                self.mock_db_driver.execute_query.call_args[0][0]
            ),
        )

        # Verify the parameters for the insert query
        self.assertEqual(
            self.mock_db_driver.execute_query.call_args[0][1][0], scooter_id
        )  # scooter_id
        self.assertEqual(
            self.mock_db_driver.execute_query.call_args[0][1][2], fault_notes
        )  # fault_notes
        # Ensure the current time is used for startDateTime, so the exact value is harder to check

    def test_resolve_scooter_fault(self):
        fault_id = 1
        resolution_notes = "Replaced battery"

        # Call the method to test
        self.fault_log_handler.resolve_scooter_fault(fault_id, resolution_notes)

        # Check that execute_query was called with the expected query and parameters
        expected_query = """
            UPDATE FaultLog
            SET endDateTime = %s, status = 'Resolved', resolution = %s
            WHERE faultID = %s;
        """
        self.assertEqual(
            self.normalize_whitespace(expected_query),
            self.normalize_whitespace(
                self.mock_db_driver.execute_query.call_args[0][0]
            ),
        )

    def test_get_open_faults(self):
        # Mock data for open faults
        self.mock_db_driver.execute_query.return_value = [
            (1, 1, "2023-09-12 12:00:00", None, "Open", None, "Battery issue"),
            (2, 2, "2023-09-13 13:00:00", None, "Open", None, "Flat tire"),
        ]

        # Call the method to test
        result = self.fault_log_handler.get_open_faults()

        # Check that execute_query was called with the expected query
        expected_query = "SELECT * FROM FaultLog WHERE status = 'Open';"
        self.assertEqual(
            self.normalize_whitespace(expected_query),
            self.normalize_whitespace(
                self.mock_db_driver.execute_query.call_args[0][0]
            ),
        )

        # Verify the result
        expected_result = [
            {
                "faultID": 1,
                "scooterID": 1,
                "startDateTime": "2023-09-12 12:00:00",
                "endDateTime": None,
                "status": "Open",
                "resolution": None,
                "faultNotes": "Battery issue",
            },
            {
                "faultID": 2,
                "scooterID": 2,
                "startDateTime": "2023-09-13 13:00:00",
                "endDateTime": None,
                "status": "Open",
                "resolution": None,
                "faultNotes": "Flat tire",
            },
        ]

        self.assertEqual(result, expected_result)

    def test_get_fault_by_scooter(self):
        scooter_id = 1
        mock_fault = {"faultID": 1, "scooterID": 1, "status": "Open"}

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = mock_fault

        # Call the method to test
        result = self.fault_log_handler.get_fault_by_scooter(scooter_id)

        # Check that execute_query was called with the expected query and parameters
        expected_query = """
            SELECT * FROM FaultLog
            WHERE scooterID = %s
            ORDER BY startDateTime DESC
            LIMIT 1;
        """
        self.assertEqual(
            self.normalize_whitespace(expected_query),
            self.normalize_whitespace(
                self.mock_db_driver.execute_query.call_args[0][0]
            ),
        )
        self.assertEqual(
            self.mock_db_driver.execute_query.call_args[0][1], (scooter_id,)
        )

        # Verify the result
        self.assertEqual(result, mock_fault)

    def test_get_fault_by_id(self):
        fault_id = 1
        mock_fault = [(1, 1, None, None, "Open", None, None)]

        # Set up the mock return value
        self.mock_db_driver.execute_query.return_value = mock_fault

        # Call the method to test
        result = self.fault_log_handler.get_fault_by_id(fault_id)

        # Check that execute_query was called with the expected query and parameters
        expected_query = """
            SELECT * 
            FROM FaultLog
            WHERE faultID = %s;
        """
        self.assertEqual(self.mock_db_driver.execute_query.call_args[0][1], (fault_id,))

        # Expected dictionary result after zipping columns with tuple values
        expected_result = {
            "faultID": 1,
            "scooterID": 1,
            "startDateTime": None,
            "endDateTime": None,
            "status": "Open",
            "resolution": None,
            "faultNotes": None,
        }
        
        # Verify the result
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
