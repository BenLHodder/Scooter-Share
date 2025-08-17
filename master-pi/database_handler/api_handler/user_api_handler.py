from flask import request, jsonify
from db_driver.user_db_handler import UserHandler

class UserAPI:
    def __init__(self, app, db_info_file):
        self.user_handler = UserHandler(db_info_file)
        self._setup_routes(app)
        
    def _setup_routes(self, app):
        # Register routes
        app.add_url_rule('/user/<email>', 'get_customer', self.get_customer, methods=['GET'])
        app.add_url_rule('/user/register', 'register_customer', self.register_customer, methods=['POST'])
        app.add_url_rule('/user/login/<email>', 'get_login_details', self.get_login_details, methods=['GET'])
        app.add_url_rule('/user/delete/<email>', 'delete_customer', self.delete_customer, methods=['DELETE'])
        app.add_url_rule('/user/update_funds', 'update_customer_funds', self.update_customer_funds, methods=['PUT'])
        app.add_url_rule('/user/customers', 'get_all_customers', self.get_all_customers, methods=['GET'])
        app.add_url_rule('/user/update_details/<email>', 'update_user_details', self.update_user_details, methods=['PUT'])
        app.add_url_rule('/user/engineers/emails', 'get_engineer_emails', self.get_engineer_emails, methods=['GET'])

    def get_customer(self, email):
        """
        API endpoint to retrieve a customer's details by their email.

        Args:
            email (str): The email of the customer.

        Returns:
            Response: JSON response containing customer details or a 404 error if not found.
        """
        result = self.user_handler.get_customer(email)
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "Customer not found."}), 404

    def register_customer(self):
        data = request.json
        try:
            self.user_handler.register_customer(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_no=data['phone_no'],
                funds=data.get('funds', 0.0),
                role=data.get('role', 'Customer')
            )
            return jsonify({"message": "Customer registered successfully."}), 201

        except Exception as e:
            return jsonify({"error": "An unexpected error occurred."}), 500

    def get_login_details(self, email):
        result = self.user_handler.get_login_details(email)
        if result:
            return jsonify({"email": result[0], "password": result[1]})
        else:
            return jsonify({"message": "User not found."}), 404

    def delete_customer(self, email):
        try:
            self.user_handler.delete_customer(email)
            return jsonify({"message": "Customer deleted successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def update_customer_funds(self):
        data = request.json
        self.user_handler.update_customer_funds(
            email=data['email'],
            new_funds=data['funds']
        )
        return jsonify({"message": "Customer funds updated successfully."})
    
    def get_all_customers(self):
        """
        API endpoint to retrieve all customers' details.

        Returns:
            Response: JSON response containing a list of all customers or an empty list if none found.
        """
        result = self.user_handler.get_all_customers()
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "No customers found."}), 404
        
    def update_user_details(self, email):
        """
        API endpoint to update a user's details.
        
        Expected JSON payload:
        {
            "password": str,
            "first_name": str,
            "last_name": str,
            "phone_no": str,
            "funds": float,
            "role": str
        }
        """
        
        data = request.json
        self.user_handler.update_user_details(
            email=email,
            password=data.get('password'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_no=data.get('phone_no'),
            funds=data.get('funds'),
            role=data.get('role')
        )
        return jsonify({"message": "User details updated successfully."}), 200
    
    def get_engineer_emails(self):
        """
        API endpoint to retrieve a list of engineer emails.

        Returns:
            Response: JSON response containing a list of engineer emails or a 404 error if none found.
        """
        result = self.user_handler.get_engineer_emails()
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "No engineers found."}), 404