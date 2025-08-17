from .api_interface import APIInterface

class UserAPI(APIInterface):
    def get_customer(self, email):
        endpoint = f"user/{email}"
        return self._send_get_request(endpoint)
    
    def get_customer_login(self, email):
        endpoint = f"user/login/{email}"
        return self._send_get_request(endpoint)

    def register_customer(self, user_data):
        endpoint = "user/register"
        return self._send_post_request(endpoint, user_data)

    def delete_customer(self, email):
        endpoint = f"user/delete/{email}"
        return self._send_delete_request(endpoint)

    def update_funds(self, update_data):
        endpoint = "user/update_funds"
        return self._send_put_request(endpoint, update_data)

    def get_all_customers(self):
        endpoint = "user/customers"
        return self._send_get_request(endpoint)
    
    def update_customer_details(self, email, update_data):
        endpoint = f"user/update_details/{email}"
        return self._send_put_request(endpoint, update_data)
    
    def get_all_engineer_emails(self):
        endpoint = "user/engineers/emails"
        return self._send_get_request(endpoint)
