from .api_interface import APIInterface

class TransactionAPI(APIInterface):
    def get_transaction(self, transaction_id):
        endpoint = f"transaction/{transaction_id}"
        return self._send_get_request(endpoint)

    def add_transaction(self, transaction_data):
        endpoint = "transaction/add_transaction"
        return self._send_post_request(endpoint, transaction_data)

    def get_customer_transactions(self, customer_id):
        endpoint = f"transaction/get_transactions/{customer_id}"
        return self._send_get_request(endpoint)