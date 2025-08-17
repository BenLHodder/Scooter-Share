from datetime import datetime
from .base_db_handler import BaseHandler

class FaultLogHandler(BaseHandler):
    def update_scooter_fault(self, scooter_id, fault_notes):
        """
        Create or update a fault entry for a scooter in the FaultLog table.

        Args:
            scooter_id (int): The ID of the scooter.
            fault_notes (str): The new fault notes to update for the scooter.
        """
        # Check if there's an open fault for the given scooter_id
        check_query = """
        SELECT faultID FROM FaultLog
        WHERE scooterID = %s AND status = 'Open';
        """
        
        result = self._db_driver.execute_query(check_query, (scooter_id,))
        
        current_time = self._to_aest(datetime.now())
        
        if result:
            # If an open fault exists, update it with new fault notes
            update_query = """
            UPDATE FaultLog
            SET faultNotes = %s
            WHERE faultID = %s;
            """
            self._db_driver.execute_query(update_query, (fault_notes, result[0][0]))
        else:
            # If no open fault exists, insert a new fault
            insert_query = """
            INSERT INTO FaultLog (scooterID, startDateTime, status, faultNotes, resolution)
            VALUES (%s, %s, 'Open', %s, NULL);
            """
            self._db_driver.execute_query(insert_query, (scooter_id, current_time, fault_notes))

    def resolve_scooter_fault(self, fault_id, resolution_notes):
        """
        Resolve a fault entry for a scooter in the FaultLog table.

        Args:
            fault_id (int): The ID of the fault.
            resolution_notes (str): Notes on how the fault was resolved.
        """
        query = """
        UPDATE FaultLog
        SET endDateTime = %s, status = 'Resolved', resolution = %s
        WHERE faultID = %s;
        """

        current_time = self._to_aest(datetime.now())
        self._db_driver.execute_query(query, (current_time, resolution_notes, fault_id))

    def get_open_faults(self):
        """
        Retrieve all open faults from the FaultLog table.

        Returns:
            list: A list of open fault entries.
        """
        query = """
        SELECT * FROM FaultLog
        WHERE status = 'Open';
        """

        try:
            result = self._db_driver.execute_query(query)
            if result:
                self.logger.info("All open faults retrieved.")
                columns = [
                    "faultID",
                    "scooterID",
                    "startDateTime",
                    "endDateTime",
                    "status",
                    "resolution",
                    "faultNotes",
                ]
                open_faults = [dict(zip(columns, row)) for row in result]
                return open_faults
            else:
                self.logger.warning("No open faults found.")
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving all open faults: {e}")
            return []

    def get_fault_by_scooter(self, scooter_id):
        """
        Retrieve the latest fault for a specific scooter.

        Args:
            scooter_id (int): The ID of the scooter.

        Returns:
            dict: A dictionary representing the latest fault entry for the scooter.
        """
        query = """
        SELECT * FROM FaultLog
        WHERE scooterID = %s
        ORDER BY startDateTime DESC
        LIMIT 1;
        """
        return self._db_driver.execute_query(query, (scooter_id,))

    def get_fault_by_id(self, fault_id):
        """
        Retrieve a fault entry by its faultID from the FaultLog table.

        Args:
            fault_id (int): The ID of the fault.

        Returns:
            dict: A dictionary containing the fault details, or None if not found.
        """
        query = """
        SELECT * 
        FROM FaultLog
        WHERE faultID = %s;
        """

        result = self._db_driver.execute_query(query, (fault_id,))

        if result:
            columns = ['faultID', 'scooterID', 'startDateTime', 'endDateTime', 'status', 'resolution', 'faultNotes']
            return dict(zip(columns, result[0]))
        return None
