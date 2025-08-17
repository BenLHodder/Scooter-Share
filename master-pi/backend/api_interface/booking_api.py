from .api_interface import APIInterface

class BookingAPI(APIInterface):
    def get_booking(self, booking_id):
        endpoint = f"booking/{booking_id}"
        return self._send_get_request(endpoint)

    def add_booking(self, booking_data):
        endpoint = "booking/add_booking"
        return self._send_post_request(endpoint, booking_data)

    def cancel_booking(self, booking_id):
        endpoint = f"booking/cancel_booking/{booking_id}"
        return self._send_delete_request(endpoint)

    def start_booking(self, booking_data):
        endpoint = "booking/start_booking"
        return self._send_put_request(endpoint, booking_data)

    def end_booking(self, booking_data):
        endpoint = "booking/end_booking"
        return self._send_put_request(endpoint, booking_data)

    def get_bookings_for_customer(self, email):
        endpoint = f"booking/get_bookings/{email}"
        return self._send_get_request(endpoint)

    def get_booked_scooters_times(self):
        endpoint = "booking/get_booked_scooters_times"
        return self._send_get_request(endpoint)
    
    def update_booking_status_complete(self, booking_id):
        endpoint = f"booking/complete/{booking_id}"
        return self._send_put_request(endpoint)
    
    def update_booking_cost(self, booking_id, booking_data):
        endpoint = f"booking/update_cost/{booking_id}"
        return self._send_put_request(endpoint, booking_data)

    def get_all_active_bookings(self):
        endpoint = "booking/active"
        return self._send_get_request(endpoint)
    
    def set_booking_googleID(self, booking_id, google_id):
        endpoint = f"booking/{booking_id}/set_googleID"
        return self._send_put_request(endpoint, google_id)
    
    def get_all_bookings_for_scooter(self, scooter_id):
        endpoint = f"booking/scooter/{scooter_id}"
        return self._send_get_request(endpoint)