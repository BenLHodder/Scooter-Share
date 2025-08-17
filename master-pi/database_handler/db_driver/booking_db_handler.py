from .base_db_handler import BaseHandler

class BookingHandler(BaseHandler):
    def add_booking(self, email, scooter_id, start_datetime, end_datetime, cost, deposit_cost, status='Active', google_id=None):
        """
        Add a new booking to the database and return the booking ID.

        Args:
            email (str): Customer's email.
            scooter_id (int): The scooter ID.
            start_datetime (datetime): Scheduled start datetime.
            end_datetime (datetime): Scheduled end datetime.
            cost (float): Booking cost.
            deposit_cost (float): Booking deposit cost.
            status (str): Booking status (e.g., 'Active', 'Complete', 'Cancelled'). Defaults to 'Active'.
            google_id (str): Optional Google ID associated with the booking. Defaults to None.

        Returns:
            int: The booking ID of the newly created booking.
        """

        start_datetime = self._to_aest(start_datetime)
        end_datetime = self._to_aest(end_datetime)

        query = """
        INSERT INTO Booking (email, scooterID, startDateTime, endDateTime, cost, depositCost, googleID, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING bookingID
        """
        params = (email, scooter_id, start_datetime, end_datetime, cost, deposit_cost, google_id, status)

        try:
            result = self._db_driver.execute_query(query, params)
            
            # Handle both tuple and int result
            if isinstance(result, tuple):
                booking_id = result[0] if result else None  # If it's a tuple, get the first element
            else:
                booking_id = result  # Otherwise, it should be an int directly
            self.logger.info(f"Booking added for customer {email} with scooter {scooter_id}. Booking ID: {booking_id}.")
            return booking_id
        except Exception as e:
            self.logger.error(f"Error adding booking for {email}: {e}")
            raise

    def cancel_booking(self, booking_id):
        """
        Cancel a booking by updating its status to 'Cancelled'.

        Args:
            booking_id (int): The ID of the booking to be canceled.
        """
        query = """
        UPDATE Booking
        SET status = 'Cancelled'
        WHERE bookingID = %s
        """
        params = (booking_id,)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Booking {booking_id} canceled successfully.")
        except Exception as e:
            self.logger.error(f"Error canceling booking {booking_id}: {e}")
            raise

    def start_booking(self, booking_id, actual_start_datetime):
        """
        Start a booking by setting the actual start datetime.

        Args:
            booking_id (int): The ID of the booking.
            actual_start_datetime (datetime): The actual start time of the booking.
        """
        
        actual_start_datetime = self._to_aest(actual_start_datetime)
        
        query = """
        UPDATE Booking
        SET actualStartDateTime = %s
        WHERE bookingID = %s
        """
        params = (actual_start_datetime, booking_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(
                f"Booking {booking_id} started at {actual_start_datetime}."
            )
        except Exception as e:
            self.logger.error(f"Error starting booking {booking_id}: {e}")
            raise

    def end_booking(self, booking_id, actual_end_datetime):
        """
        End a booking by setting the actual end datetime.

        Args:
            booking_id (int): The ID of the booking.
            actual_end_datetime (datetime): The actual end time of the booking.
        """
        actual_end_datetime = self._to_aest(actual_end_datetime)
        
        query = """
        UPDATE Booking
        SET actualEndDateTime = %s
        WHERE bookingID = %s
        """
        params = (actual_end_datetime, booking_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Booking {booking_id} ended at {actual_end_datetime}.")
        except Exception as e:
            self.logger.error(f"Error ending booking {booking_id}: {e}")
            raise

    def get_booking(self, booking_id):
        """
        Retrieve all details for a booking from the database by booking ID.

        Args:
            booking_id (int): The ID of the booking to look up.

        Returns:
            dict: A dictionary containing all the booking's details if found, otherwise None.
        """
        query = "SELECT * FROM Booking WHERE bookingID = %s"
        params = (booking_id,)

        try:
            result = self._db_driver.execute_query(query, params)
            if result:
                self.logger.info(
                    f"Booking details retrieved for booking ID {booking_id}."
                )
                columns = [
                    "email",
                    "scooterID",
                    "bookingID",
                    "startDateTime",
                    "endDateTime",
                    "actualStartDateTime",
                    "actualEndDateTime",
                    "cost",
                    "depositCost",
                    "googleID",
                    "status"
                ]
                booking_data = dict(zip(columns, result[0]))
                return booking_data
            else:
                self.logger.warning(f"No booking found with ID: {booking_id}")
                return None
        except Exception as e:
            self.logger.error(
                f"Error retrieving booking details for ID {booking_id}: {e}"
            )
            return None

    def get_all_bookings_for_customer(self, email):
        """
        Retrieve all bookings for a specific customer.

        Args:
            email (str): Customer's email.

        Returns:
            list: List of bookings for the customer, where each booking is a dictionary.
        """
        query = "SELECT * FROM Booking WHERE email = %s ORDER BY startDateTime DESC"
        params = (email,)

        try:
            results = self._db_driver.execute_query(query, params)

            columns = [
                "email",
                "scooterID",
                "bookingID",
                "startDateTime",
                "endDateTime",
                "actualStartDateTime",
                "actualEndDateTime",
                "cost",
                "depositCost",
                "googleID",
                "status"
            ]
            bookings = [dict(zip(columns, row)) for row in results]

            self.logger.info(f"Retrieved all bookings for customer {email}.")
            return bookings
        except Exception as e:
            self.logger.error(f"Error retrieving bookings for {email}: {e}")
            raise

    def get_all_booked_scooters_and_times(self):
        """
        Retrieve all booked scooters, their time slots and their status.

        Returns:
            list: List of scooters, their booked time slots and their status.
        """
        query = "SELECT scooterID, startDateTime, endDateTime, status FROM Booking"

        try:
            results = self._db_driver.execute_query(query)
            columns = [
                "scooterID",
                "startDateTime",
                "endDateTime",
                "status",
            ]
            results = [dict(zip(columns, row)) for row in results]
            self.logger.info("Retrieved all booked scooters and their time slots.")
            return results
        except Exception as e:
            self.logger.error(f"Error retrieving booked scooters and times: {e}")
            raise

    def set_booking_complete(self, booking_id):
        """
        Set a booking's status to 'Complete'.

        Args:
            booking_id (int): The ID of the booking to complete.
        """
        query = """
        UPDATE Booking
        SET status = 'Complete'
        WHERE bookingID = %s
        """
        params = (booking_id,)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Booking {booking_id} marked as complete.")
        except Exception as e:
            self.logger.error(f"Error marking booking {booking_id} as complete: {e}")
            raise
        
    def update_booking_cost(self, booking_id, new_cost):
        """
        Update the cost of a booking.

        Args:
            booking_id (int): The ID of the booking to update.
            new_cost (float): The new cost to set for the booking.
        """
        query = """
        UPDATE Booking
        SET cost = %s
        WHERE bookingID = %s
        """
        params = (new_cost, booking_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Booking {booking_id} cost updated to {new_cost}.")
        except Exception as e:
            self.logger.error(f"Error updating cost for booking {booking_id}: {e}")
            raise

    def get_all_active_bookings(self):
        """
        Retrieve all active bookings from the database.

        Returns:
            list: A list of active bookings, where each booking is a dictionary.
        """
        query = "SELECT * FROM Booking WHERE status = 'Active'"
        
        try:
            results = self._db_driver.execute_query(query)
            
            if results:
                columns = [
                    "email",
                    "scooterID",
                    "bookingID",
                    "startDateTime",
                    "endDateTime",
                    "actualStartDateTime",
                    "actualEndDateTime",
                    "cost",
                    "depositCost",
                    "googleID",
                    "status"
                ]
                active_bookings = [dict(zip(columns, row)) for row in results]
                self.logger.info("Retrieved all active bookings.")
                return active_bookings
            else:
                self.logger.info("No active bookings found.")
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving active bookings: {e}")
            raise

    def set_booking_googleID(self, booking_id, google_id):
        """
        Add the google ID of a booking to the database.

        Args:
            booking_id (int): The ID of the booking to be amend.
            google_id (str): The google ID to be added.
        """
        query = """
        UPDATE Booking
        SET googleID = %s
        WHERE bookingID = %s
        """
        params = (google_id, booking_id)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Booking {booking_id} updated successfully.")
        except Exception as e:
            self.logger.error(f"Error updating booking {booking_id}: {e}")
            raise
        
    def get_all_bookings_for_scooter(self, scooter_id):
        """
        Retrieve all bookings for a specific scooter.

        Args:
            scooter_id (int): The ID of the scooter.

        Returns:
            list: List of bookings for the scooter, where each booking is a dictionary.
        """
        query = "SELECT * FROM Booking WHERE scooterID = %s ORDER BY startDateTime DESC"
        params = (scooter_id,)

        try:
            results = self._db_driver.execute_query(query, params)
            
            columns = [
                "email",
                "scooterID",
                "bookingID",
                "startDateTime",
                "endDateTime",
                "actualStartDateTime",
                "actualEndDateTime",
                "cost",
                "depositCost",
                "googleID",
                "status"
            ]
            bookings = [dict(zip(columns, row)) for row in results]

            self.logger.info(f"Retrieved all bookings for scooter {scooter_id}.")
            return bookings
        except Exception as e:
            self.logger.error(f"Error retrieving bookings for scooter {scooter_id}: {e}")
            raise
