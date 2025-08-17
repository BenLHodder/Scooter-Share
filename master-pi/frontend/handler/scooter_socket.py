from .socket_manager import SocketManager


class ScooterSocket:
    def __init__(self):
        self.socket_manager = SocketManager()

    def get_scooter_details(self, scooter_id):
        """Get Scooter Details"""

        message = {
            "command": "GSD",
            "payload": {"scooter_id": scooter_id},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def get_all_scooters(self):
        """Get all Scooters"""

        message = {
            "command": "GAS",
            "payload": {},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def add_scooter_fault_notes(self, scooter_id, fault_notes):
        """Send in scooter fault"""

        message = {
            "command": "RSF",
            "payload": {
                "scooter_id": scooter_id,
                "fault_notes": fault_notes,
            },
        }

        response = self.socket_manager.send_and_receive(message)
        return response

    def find_my_scooter(self, scooter_id):
        """Find the location of a scooter"""

        message = {"command": "FMS", "payload": {"scooter_id": scooter_id}}

        response = self.socket_manager.send_and_receive(message)
        return response
    
    def update_scooter(self, updated_data):
        """Update the scooter information"""
        
        message= {"command": "USD", "payload": updated_data}
        
        response = self.socket_manager.send_and_receive(message)
        return response
