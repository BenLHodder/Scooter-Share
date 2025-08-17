from .socket_manager import SocketManager


class UserSocket:
    def __init__(self):
        self.socket_manager = SocketManager()

    def register_user(self, email, password, first_name, last_name, phone_no, funds, role):
        """Send Registration to Master Pi"""

        message = {
            "command": "RNC",
            "payload": {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "phone_no": phone_no,
                "funds": funds,
                "role": role,
            },
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def login_user(self, email):
        """Send login to the Master Pi"""

        message = {
            "command": "GLD",
            "payload": {"email": email},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def retrieve_user(self, email):
        """Get user details from Master Pi"""

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

    def user_forgot_password(self, email, url):
        """Send email to user about forgotten password"""

        message = {
            "command": "FP",
            "payload": {"email": email, "url": url},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def update_user_details(
        self, email, password, first_name, last_name, phone_no, funds, role
    ):
        """Update customer password"""

        message = {
            "command": "UCD",
            "payload": {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "phone_no": phone_no,
                "funds": funds,
                "role": role,
            },
        }
        response = self.socket_manager.send_and_receive(message)
        return response
