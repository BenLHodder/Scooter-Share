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
    
    def get_all_bookings_for_scooter(self, scooter_id):
        """Get all booking details for a specific scooter"""

        message = {
            "command": "GABFS",
            "payload": {"scooter_id": scooter_id},
        }
        
        response = self.socket_manager.send_and_receive(message)
        return response
