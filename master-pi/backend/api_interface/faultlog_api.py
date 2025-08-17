from .api_interface import APIInterface

class FaultLogAPI(APIInterface):
    def get_fault_by_id(self, fault_id):
        """Retrieve a fault entry by its faultID."""
        endpoint = f"fault/{fault_id}"
        return self._send_get_request(endpoint)

    def get_open_faults(self):
        """Retrieve all open faults."""
        endpoint = "fault/open_faults"
        return self._send_get_request(endpoint)

    def get_fault_by_scooter(self, scooter_id):
        """Retrieve the latest fault for a specific scooter."""
        endpoint = f"fault/scooter/{scooter_id}"
        return self._send_get_request(endpoint)

    def update_scooter_fault(self, fault_data):
        """Create or update a fault entry for a scooter."""
        endpoint = "fault/update_scooter_fault"
        return self._send_put_request(endpoint, fault_data)

    def resolve_scooter_fault(self, fault_id, resolution_data):
        """Resolve a fault entry for a scooter."""
        endpoint = f"fault/resolve_scooter_fault/{fault_id}"
        return self._send_put_request(endpoint, resolution_data)
