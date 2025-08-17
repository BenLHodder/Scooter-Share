from .socket_manager import SocketManager


class BookingSocket:
    def __init__(self):
        self.socket_manager = SocketManager()

    def add_booking(
        self, email, scooter_id, start_datetime, end_datetime, deposit_cost, cost
    ):
        """Add a new booking for a customer"""

        message = {
            "command": "AB",
            "payload": {
                "email": email,
                "scooter_id": scooter_id,
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "deposit_cost": deposit_cost,
                "googleID": None,
                "cost": cost,
            },
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def cancel_booking(self, booking_id):
        """Cancel customer booking"""

        message = {
            "command": "CB",
            "payload": {"booking_id": booking_id},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def get_all_booked_scooter_times(self):
        """Get all Booked Scooter Times"""

        message = {
            "command": "GABS",
            "payload": {},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def get_booking_details(self, booking_id):
        """Get details on specific bookings"""

        message = {
            "command": "GBD",
            "payload": {"booking_id": booking_id},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def get_bookings_for_customer(self, email):
        """Get all booking details for a specific customer"""

        message = {
            "command": "GAB",
            "payload": {"email": email},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def set_booking_google_id(self, booking_id, google_id):
        """Set the Google Calendar Event ID to the Booking"""

        message = {
            "command": "SBG",
            "payload": {"booking_id": booking_id, "google_id": google_id},
        }
        response = self.socket_manager.send_and_receive(message)
        return response
