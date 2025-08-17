from .base_db_handler import BaseHandler

class TransactionHandler(BaseHandler):
    def add_transaction(self, email, transaction_amount, transaction_datetime):
        """
        Add a new transaction to the Transaction table.

        Args:
            email (str): The customer's email associated with the transaction.
            transaction_amount (float): The amount of the transaction.
            transaction_datetime (datetime): The date and time of the transaction.
        """
        transaction_datetime = self._to_aest(transaction_datetime)
        
        query = """
        INSERT INTO Transaction (email, datetime, transactionAmount)
        VALUES (%s, %s, %s)
        """
        params = (email, transaction_datetime, transaction_amount)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"Transaction added for customer {email} with amount {transaction_amount}.")
        except Exception as e:
            self.logger.error(f"Error adding transaction for {email}: {e}")
            raise
        
    def get_transaction(self, transaction_id):
        """
        Retrieve all details for a transaction from the database by transaction ID.

        Args:
            transaction_id (int): The ID of the transaction to look up.

        Returns:
            dict: A dictionary containing all the transaction's details if found, otherwise None.
        """
        query = "SELECT * FROM Transaction WHERE transactionID = %s"
        params = (transaction_id,)

        try:
            result = self._db_driver.execute_query(query, params)
            if result:
                self.logger.info(f"Transaction details retrieved for transaction ID {transaction_id}.")
                columns = ['email', 'transactionID', 'datetime', 'transactionAmount']
                transaction_data = dict(zip(columns, result[0]))
                return transaction_data
            else:
                self.logger.warning(f"No transaction found with ID: {transaction_id}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving transaction details for ID {transaction_id}: {e}")
            return None

    def get_all_transactions_for_customer(self, email):
        """
        Retrieve all transactions associated with a specific customer.

        Args:
            email (str): The email of the customer whose transactions are to be retrieved.

        Returns:
            list: A list of dictionaries containing transaction details for the customer.
        """
        query = "SELECT * FROM Transaction WHERE email = %s"
        params = (email,)

        try:
            results = self._db_driver.execute_query(query, params)
            if results:
                self.logger.info(f"Transactions retrieved for customer {email}.")
                columns = ['email', 'transactionID', 'datetime', 'transactionAmount']
                transactions = [dict(zip(columns, row)) for row in results]
                return transactions
            else:
                self.logger.warning(f"No transactions found for customer: {email}")
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving transactions for customer {email}: {e}")
            return []