from flask import request, jsonify
from db_driver.transaction_db_handler import TransactionHandler

class TransactionAPI:
    def __init__(self, app, db_info_file):
        self.transaction_handler = TransactionHandler(db_info_file)
        self._setup_routes(app)
        
    def _setup_routes(self, app):
        # Register routes
        app.add_url_rule('/transaction/<int:transaction_id>', 'get_transaction', self.get_transaction, methods=['GET'])
        app.add_url_rule('/transaction/add_transaction', 'add_transaction', self.add_transaction, methods=['POST'])
        app.add_url_rule('/transaction/get_transactions/<string:email>', 'get_transactions_for_customer', self.get_transactions_for_customer, methods=['GET'])
    
    def get_transaction(self, transaction_id):
        """
        API endpoint to retrieve a transaction's details by its ID.

        Args:
            transaction_id (int): The ID of the transaction.

        Returns:
            Response: JSON response containing transaction details or a 404 error if not found.
        """
        result = self.transaction_handler.get_transaction(transaction_id)
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "Transaction not found."}), 404

    def add_transaction(self):
        data = request.json
        self.transaction_handler.add_transaction(
            email=data['email'],
            transaction_amount=data['transaction_amount'],
            transaction_datetime=data['transaction_datetime']
        )
        return jsonify({"message": "Transaction added successfully."})
    
    def get_transactions_for_customer(self, email):
        """
        API endpoint to retrieve all transactions associated with a specific customer.

        Args:
            email (str): The email of the customer whose transactions are to be retrieved.

        Returns:
            Response: JSON response containing the list of transactions or an error message.
        """
        try:
            transactions = self.transaction_handler.get_all_transactions_for_customer(email)
            return jsonify({"transactions": transactions})
        except Exception as e:
            return jsonify({"error": str(e)}), 400