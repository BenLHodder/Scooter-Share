from api_interface.user_api import UserAPI
from api_interface.booking_api import BookingAPI
from api_interface.transaction_api import TransactionAPI
from api_interface.scooter_api import ScooterAPI
from api_interface.faultlog_api import FaultLogAPI

class api_handler:
    def __init__(self):
        self.__base_url = "http://localhost:8080"
        
        # Initialize API clients
        self.__user_api = UserAPI(self.__base_url)
        self.__booking_api = BookingAPI(self.__base_url)
        self.__transaction_api = TransactionAPI(self.__base_url)
        self.__scooter_api = ScooterAPI(self.__base_url)
        self.__faultlog_api = FaultLogAPI(self.__base_url)
    
    ###
    # USER API
    ###
    def get_customer_details(self, email):
        return self.__user_api.get_customer(email)
    
    def register_new_customer(self, user_data):
        return self.__user_api.register_customer(user_data)
    
    def get_login_details(self, email):
        return self.__user_api.get_customer_login(email)
        
    def delete_customer(self, email):
        return self.__user_api.delete_customer(email)
    
    def update_customer_funds(self, customer_data):
        return self.__user_api.update_funds(customer_data)
    
    def get_all_customers(self):
        return self.__user_api.get_all_customers()
    
    def update_customer_details(self, email, customer_data):
        return self.__user_api.update_customer_details(email, customer_data)
    
    def get_all_engineer_emails(self):
        return self.__user_api.get_all_engineer_emails()
    
    ###
    # SCOOTER API
    ###
    
    def get_scooter_details(self, scooter_id):
        return self.__scooter_api.get_scooter(scooter_id)
    
    def set_scooter_status(self, scooter_data):
        return self.__scooter_api.update_scooter_status(scooter_data)
    
    def get_all_scooters(self):
        return self.__scooter_api.get_all_scooters()
    
    def update_scooter_location(self, scooter_id, scooter_data):
        return self.__scooter_api.update_scooter_location(scooter_id, scooter_data)
    
    def update_scooter_ip_address(self, scooter_id, scooter_data):
        return self.__scooter_api.update_scooter_ip_address(scooter_id, scooter_data)
    
    def update_scooter_details(self, scooter_id, scooter_data):
        return self.__scooter_api.update_scooter_details(scooter_id, scooter_data)
    
    ###
    # BOOKING API 
    ###
    def cancel_booking(self, booking_id):
        return self.__booking_api.cancel_booking(booking_id)
    
    def add_booking(self, booking_data):
        return self.__booking_api.add_booking(booking_data)
    
    def get_booking(self, booking_id):
        return self.__booking_api.get_booking(booking_id)
    
    def get_all_bookings(self, email):
        return self.__booking_api.get_bookings_for_customer(email)
    
    def get_all_bookings_for_scooters(self):
        return self.__booking_api.get_booked_scooters_times()
    
    def start_booking(self, payload):
        return self.__booking_api.start_booking(payload)
    
    def end_booking(self, payload):
        return self.__booking_api.end_booking(payload)

    def set_booking_status_complete(self, booking_id):
        return self.__booking_api.update_booking_status_complete(booking_id)
    
    def update_booking_cost(self, booking_id, booking_data):
        return self.__booking_api.update_booking_cost(booking_id, booking_data)
    
    def get_active_bookings(self):
        return self.__booking_api.get_all_active_bookings()
    
    def set_booking_googleID(self, booking_id, google_id):
        return self.__booking_api.set_booking_googleID(booking_id, google_id)
    
    def get_all_bookings_for_scooter(self, scooter_id):
        return self.__booking_api.get_all_bookings_for_scooter(scooter_id)
    
    ###
    # TRANSACTION API
    ###
    def get_transaction(self, transaction_id):
        return self.__transaction_api.get_transaction(transaction_id)
    
    def add_transaction(self, transaction_data):
        return self.__transaction_api.add_transaction(transaction_data)
    
    def get_customer_transactions(self, customer_id):
        return self.__transaction_api.get_customer_transactions(customer_id)

    ###
    # FAULT LOG API
    ###
    def get_fault_by_id(self, fault_id):
        return self.__faultlog_api.get_fault_by_id(fault_id)

    def get_open_faults(self):
        return self.__faultlog_api.get_open_faults()

    def get_fault_by_scooter(self, scooter_id):
        return self.__faultlog_api.get_fault_by_scooter(scooter_id)

    def update_scooter_fault(self, fault_data):
        return self.__faultlog_api.update_scooter_fault(fault_data)

    def resolve_scooter_fault(self, fault_id, resolution_data):
        return self.__faultlog_api.resolve_scooter_fault(fault_id, resolution_data)
