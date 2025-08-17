from .socket_manager import SocketManager


class FaultLogSocket:
    def __init__(self):
        self.socket_manager = SocketManager()

    def add_or_update_scooter_fault(self, scooter_id, fault_notes):
        """Send in orupdate scooter fault"""

        message = {
            "command": "RSF",
            "payload": {
                "scooter_id": scooter_id,
                "fault_notes": fault_notes,
            },
        }

        response = self.socket_manager.send_and_receive(message)
        return response

    def resolve_scooter_fault(self, fault_id, resolution_notes):
        """Resolve Scooter Fault"""

        message = {
            "command": "RESF",
            "payload": {
                "fault_id": fault_id,
                "resolution_notes": resolution_notes,
            },
        }

        response = self.socket_manager.send_and_receive(message)
        return response

    def get_open_scooter_faults(self):
        """Get all open scooter faults"""

        message = {
            "command": "GOF",
            "payload": {},
        }

        response = self.socket_manager.send_and_receive(message)
        return response

    def get_latest_fault_by_scooter(self, scooter_id):
        """Get Latest Fault by Scooter ID"""

        message = {
            "command": "GFBS",
            "payload": {
                "scooter_id": scooter_id,
            },
        }

        response = self.socket_manager.send_and_receive(message)
        return response

    def get_fault_by_id(self, fault_id):
        """Retrieve a fault entry by its fault ID"""

        message = {
            "command": "GFBI",
            "payload": {
                "fault_id": fault_id,
            },
        }

        response = self.socket_manager.send_and_receive(message)
        return response
