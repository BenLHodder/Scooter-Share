# api_interface/scooter_api.py
from .api_interface import APIInterface

class ScooterAPI(APIInterface):
    def get_scooter(self, scooter_id):
        endpoint = f"scooter/{scooter_id}"
        return self._send_get_request(endpoint)

    def update_scooter_status(self, scooter_data):
        endpoint = "scooter/update_scooter_status"
        return self._send_put_request(endpoint, scooter_data)
    
    def get_all_scooters(self):
        endpoint = "scooter/scooters"
        return self._send_get_request(endpoint)
    
    def update_scooter_location(self, scooter_id, scooter_data):
        endpoint = f"scooter/update_location/{scooter_id}"
        return self._send_put_request(endpoint, scooter_data)
    
    def update_scooter_ip_address(self, scooter_id, scooter_data):
        endpoint = f"scooter/update_ip_address/{scooter_id}"
        return self._send_put_request(endpoint, scooter_data)
    
    def update_scooter_details(self, scooter_id, scooter_data):
        endpoint = f"scooter/update_details/{scooter_id}"
        return self._send_put_request(endpoint, scooter_data)