from .base_db_handler import BaseHandler

class UserHandler(BaseHandler):
    def register_customer(self, email, password, first_name, last_name, phone_no, funds=0.0, role='Customer'):
        """
        Register a new user in the database by inserting their details.

        Args:
            email (str): User's email (primary key).
            password (str): User's password (hashed).
            first_name (str): User's first name.
            last_name (str): User's last name.
            phone_no (str): User's phone number.
            funds (float): Initial user funds (default is 0.0).
            role (str): User's role (default is 'Customer').
        """
        query = """
        INSERT INTO SystemUser (email, password, firstName, lastName, phoneNo, funds, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (email, password, first_name, last_name, phone_no, funds, role)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"User {email} successfully registered.")
            return {"message": "User registered successfully."}, 201
            
        except Exception as e:
            # Log detailed information for unexpected exceptions
            self.logger.error(f"Exception type: {type(e).__name__}")
            self.logger.error(f"Error message: {str(e)}")
            self.logger.error("Traceback:", exc_info=True)
            
            # Rollback the transaction for any other exceptions
            if hasattr(self._db_driver.connection, 'rollback'):
                self._db_driver.connection.rollback()
            return {"error": "An unexpected error occurred."}, 500

    def get_login_details(self, email):
        """
        Retrieve a user's login details (email and password) from the database.

        Args:
            email (str): User's email to look up.

        Returns:
            tuple: A tuple containing the user's email and password.
        """
        query = "SELECT email, password FROM SystemUser WHERE email = %s"
        params = (email,)

        try:
            result = self._db_driver.execute_query(query, params)
            if result:
                self.logger.info(f"Login details retrieved for {email}.")
                return result[0]  # Assuming result[0] is (email, password)
            else:
                self.logger.warning(f"No user found with email: {email}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving login details for {email}: {e}")
            return None

    def delete_customer(self, email):
        """
        Remove a customer from the User table based on the provided email.
        
        Args:
            email (str): The email of the customer to be removed.
        """
        query = "DELETE FROM SystemUser WHERE email = %s"
        params = (email,)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"User with email {email} deleted successfully.")
        except Exception as e:
            self.logger.error(f"Error deleting customer with email {email}: {e}")
            raise
        
    def update_customer_funds(self, email, new_funds):
        """
        Update the funds of a customer in the User table.

        Args:
            email (str): The customer's email.
            new_funds (float): The updated funds value.
        """
        query = """
        UPDATE SystemUser
        SET funds = %s
        WHERE email = %s
        """
        params = (new_funds, email)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"User {email}'s funds updated to {new_funds}.")
        except Exception as e:
            self.logger.error(f"Error updating funds for customer {email}: {e}")
            raise

    def get_customer(self, email):
        """
        Retrieve all details for a customer from the database by email.

        Args:
            email (str): The email of the customer to look up.

        Returns:
            dict: A dictionary containing all the customer's details if found, otherwise None.
        """
        query = "SELECT * FROM SystemUser WHERE email = %s"
        params = (email,)

        try:
            result = self._db_driver.execute_query(query, params)
            if result:
                self.logger.info(f"User details retrieved for {email}.")
                columns = ['email', 'password', 'firstName', 'lastName', 'phoneNo', 'funds', 'role']
                customer_data = dict(zip(columns, result[0]))  # Converting row into a dictionary
                return customer_data
            else:
                self.logger.warning(f"No customer found with email: {email}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving customer details for {email}: {e}")
            return None

    def get_all_customers(self):
        """
        Retrieve all customers from the SystemUser table.

        Returns:
            list: A list of dictionaries, each containing details of a customer.
        """
        query = "SELECT * FROM SystemUser WHERE role = %s"
        params = ('Customer',)

        try:
            results = self._db_driver.execute_query(query, params)
            if results:
                self.logger.info(f"Retrieved {len(results)} customers.")
                columns = ['email', 'password', 'firstName', 'lastName', 'phoneNo', 'funds', 'role']
                customers = [dict(zip(columns, result)) for result in results]  # Convert each row to a dictionary
                return customers
            else:
                self.logger.warning("No customers found.")
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving all customers: {e}")
            return []
        
    def update_user_details(self, email, password, first_name, last_name, phone_no, funds, role):
        """
        Update all details for a given user in the SystemUser table.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            phone_no (str): The phone number of the user.
            funds (float): The amount of funds the user has.
            role (str): The role of the user (e.g., 'Customer', 'Admin', 'Engineer').
        """
        query = """
        UPDATE SystemUser
        SET password = %s, firstName = %s, lastName = %s, phoneNo = %s, funds = %s, role = %s
        WHERE email = %s
        """
        params = (password, first_name, last_name, phone_no, funds, role, email)

        try:
            self._db_driver.execute_query(query, params)
            self.logger.info(f"User {email} details updated.")
        except Exception as e:
            self.logger.error(f"Error updating details for user {email}: {e}")
            raise
        
    def get_engineer_emails(self):
        """
        Retrieve all email addresses for users with the role 'Engineer'.

        Returns:
            list: A list of email addresses for users with the 'Engineer' role.
        """
        query = "SELECT email FROM SystemUser WHERE role = %s"
        params = ('Engineer',)

        try:
            results = self._db_driver.execute_query(query, params)
            if results:
                self.logger.info(f"Retrieved {len(results)} engineer emails.")
                engineer_emails = [result[0] for result in results]  # Extract the email from each result row
                return engineer_emails
            else:
                self.logger.warning("No engineers found.")
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving engineer emails: {e}")
            return []
