from .base_db_handler import BaseHandler

class ScooterHandler(BaseHandler):
    def update_scooter_status(self, scooter_id, new_status):
        """
        Update the status of a scooter in the Scooter table.

        Args:
            scooter_id (int): The ID of the scooter.
            new_status (str): The new status of the scooter (e.g., 'available', 'in use', 'maintenance').
        """
        query = """
        UPDATE Scooter
        SET status = %s
        WHERE scooterID = %s
        """
        params = (new_status, scooter_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Scooter {scooter_id} status updated to {new_status}.")
        except Exception as e:
            self.logger.error(f"Error updating status for scooter {scooter_id}: {e}")
            raise
        
    def get_scooter(self, scooter_id):
        """
        Retrieve all details for a scooter from the database by scooter ID.

        Args:
            scooter_id (int): The ID of the scooter to look up.

        Returns:
            dict: A dictionary containing all the scooter's details if found, otherwise None.
        """
        query = "SELECT * FROM Scooter WHERE scooterID = %s"
        params = (scooter_id,)

        try:
            result = self._db_driver.execute_query(query, params)
            if result:
                self.logger.info(f"Scooter details retrieved for scooter ID {scooter_id}.")
                columns = ['scooterID', 'make', 'colour', 'longitude', 'latitude', 'costMin',
                           'batteryPercentage', 'status', 'ipAddress', 'faultNotes']
                scooter_data = dict(zip(columns, result[0]))
                return scooter_data
            else:
                self.logger.warning(f"No scooter found with ID: {scooter_id}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving scooter details for ID {scooter_id}: {e}")
            return None
    

    def get_all_scooters(self):
        """
        Retrieve all scooter records from the Scooter table.

        Returns:
            list: A list of dictionaries containing scooter details, or an empty list if no scooters are found.
        """
        query = "SELECT * FROM Scooter"

        try:
            result = self._db_driver.execute_query(query)
            if result:
                self.logger.info("Scooter details retrieved for all scooters.")
                columns = ['scooterID', 'make', 'colour', 'longitude', 'latitude', 'costMin',
                        'batteryPercentage', 'status', 'ipAddress', 'faultNotes']
                scooters = [dict(zip(columns, row)) for row in result]
                return scooters
            else:
                self.logger.warning("No scooters found.")
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving all scooters: {e}")
            return []
        
    def update_scooter_location(self, scooter_id, latitude, longitude):
        """
        Update the location (latitude and longitude) of a scooter in the Scooter table.

        Args:
            scooter_id (int): The ID of the scooter.
            latitude (float): The new latitude of the scooter.
            longitude (float): The new longitude of the scooter.
        """
        query = """
        UPDATE Scooter
        SET latitude = %s, longitude = %s
        WHERE scooterID = %s
        """
        params = (latitude, longitude, scooter_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Scooter {scooter_id} location updated to latitude: {latitude}, longitude: {longitude}.")
        except Exception as e:
            self.logger.error(f"Error updating location for scooter {scooter_id}: {e}")
            raise

    def update_scooter_ip_address(self, scooter_id, new_ip_address):
        """
        Update the IP address of a scooter in the Scooter table.

        Args:
            scooter_id (int): The ID of the scooter.
            new_ip_address (str): The new IP address of the scooter.
        """
        query = """
        UPDATE Scooter
        SET ipAddress = %s
        WHERE scooterID = %s
        """
        params = (new_ip_address, scooter_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Scooter {scooter_id} IP address updated to {new_ip_address}.")
        except Exception as e:
            self.logger.error(f"Error updating IP address for scooter {scooter_id}: {e}")
            raise

    def update_scooter_details(self, scooter_id, make, colour, latitude, longitude, cost_min, battery_percentage, status, ip_address):
        """
        Update all details for a given scooter in the Scooter table.

        Args:
            scooter_id (int): The ID of the scooter.
            make (str): The make of the scooter.
            colour (str): The colour of the scooter.
            latitude (float): The latitude of the scooter.
            longitude (float): The longitude of the scooter.
            cost_min (float): The cost per minute of using the scooter.
            battery_percentage (int): The battery percentage of the scooter.
            status (str): The current status of the scooter.
            ip_address (str): The IP address of the scooter.
        """
        query = """
        UPDATE Scooter
        SET make = %s, colour = %s, latitude = %s, longitude = %s, costMin = %s, 
            batteryPercentage = %s, status = %s, ipAddress = %s
        WHERE scooterID = %s
        """
        params = (make, colour, latitude, longitude, cost_min, battery_percentage, status, ip_address, scooter_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Scooter {scooter_id} details updated.")
        except Exception as e:
            self.logger.error(f"Error updating details for scooter {scooter_id}: {e}")
            raise