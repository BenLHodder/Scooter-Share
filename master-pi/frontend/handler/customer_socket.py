from .socket_manager import SocketManager


class CustomerSocket:
    def __init__(self):
        self.socket_manager = SocketManager()

    def register_customer(self, email, password, first_name, last_name, phone_no):
        """Send Registration to Master Pi"""

        message = {
            "command": "RNC",
            "payload": {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "phone_no": phone_no,
            },
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def login_customer(self, email):
        """Send login to the Master Pi"""

        message = {
            "command": "GLD",
            "payload": {"email": email},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def retrieve_customer(self, email):
        """Get customer details from Master Pi"""

        message = {
            "command": "GCD",
            "payload": {"email": email},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def update_customer_funds(self, email, funds):
        """Update customer funds"""

        message = {
            "command": "UCF",
            "payload": {"email": email, "funds": funds},
        }
        response = self.socket_manager.send_and_receive(message)
        return response
    
    def get_all_customers(self):
        """Get all customer details from Master Pi"""

        message = {
            "command": "GAC",
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def update_customer(self, updated_data):
        """Update customer details in Master Pi"""
        message = {
            "command": "UCD",
            "payload": updated_data,
        }
        
        response = self.socket_manager.send_and_receive(message)
        return response