from .socket_manager import SocketManager


class TransactionSocket:
    def __init__(self):
        self.socket_manager = SocketManager()

    def get_transaction_details(self, transaction_id):
        """Get Transaction Details"""

        message = {
            "command": "GTD",
            "payload": {"transaction_id": transaction_id},
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def add_new_transaction(self, email, transaction_amount, transaction_datetime):
        """Add New Transaction"""

        message = {
            "command": "ANT",
            "payload": {
                "email": email,
                "transaction_amount": transaction_amount,
                "transaction_datetime": transaction_datetime,
            },
        }
        response = self.socket_manager.send_and_receive(message)
        return response

    def get_all_customer_transactions(self, email):
        """Get all transactions for a customer"""

        message = {
            "command": "GACT",
            "payload": {
                "email": email,
            },
        }
        response = self.socket_manager.send_and_receive(message)
        return response
