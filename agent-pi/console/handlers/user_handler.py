import json
import threading
import time
import pytz
from datetime import datetime, timedelta
from dateutil import parser

AEST = pytz.timezone('Australia/Sydney')

class user_handler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(user_handler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, socket, scooter_handler):
        if not hasattr(self, 'initialised'):
            self.__email = None
            self.__hash = None
            self.__logged_in = False
            self.__status = "Locked"
            self.__funds = 0.0
            self.__phone_no = None
            self.__booking_id = None
            self.__scooter_num = None
            self.__start_time = None
            self.__end_time = None
            self.__sock = socket
            self.__scooter_handler = scooter_handler
            self.initialised = True
        
    def login(self, email: str, pass_hash: str, scooter_num):
        """
        Logs in a user on this scooter, given that the user has enough funds.

        :param email: The email of the user to log in
        :param scooter_num: The number of the scooter to log in to
        :return: True if the user was successfully logged in, False if the user has no funds or an error occurred
        """
        self.__email = email
        self.__hash = pass_hash
        booking_id = self.__sock.get_booking_id(self.__email, scooter_num)
        details = self.__sock.get_customer_details(self.__email)
        try:
            booking_dict = json.loads(booking_id)
            if 'error' in booking_dict:
                if booking_dict['error'] != "No booking found":
                    print(f"Error: {booking_dict['error']}")
                    return False
                elif booking_dict['error'] == "No booking found":
                    AEST = pytz.timezone('Australia/Sydney')
                    add_booking = {
                        "email": self.__email,
                        "scooter_id": scooter_num,
                        "start_datetime": datetime.now(AEST).isoformat(),
                        "end_datetime": (datetime.now(AEST) + timedelta(minutes=10)).isoformat(),
                        "cost": 0.0,
                        "googleID": None,
                        "deposit_cost": 0.0,
                    }
                    self.__sock.set_scooter_status("In Use", scooter_num)
                    self.__sock.add_booking(add_booking)
                    
                    booking_id = self.__sock.get_booking_id(self.__email, scooter_num)
                    if isinstance(booking_id, str):
                        booking_id = json.loads(booking_id)
                    
                    booking_dict["bookingID"] = booking_id.get("bookingID")
                else:
                   print(booking_dict) 
        
            self.__booking_id = booking_dict["bookingID"]
            booking_info = self.__sock.get_booking_details(self.__booking_id)
            booking_dict = json.loads(booking_info)
            if 'error' in booking_dict:
                if booking_dict['error'] != "No booking found":
                    print(f"Error: {booking_dict['error']}")
                    return False  
            self.__start_time = self.parse_iso8601(booking_dict.get("startDateTime"))
            self.__end_time = self.parse_iso8601(booking_dict.get("endDateTime"))
            
            details_dict = json.loads(details)  # Convert JSON string to dictionary
            
            self.__phone_no = details_dict["phoneNo"]
            self.__funds = details_dict["funds"]
            
            logout_thread = threading.Thread(target=self.logout_timer)
            logout_thread.start()
            
            if self.__funds >= 5:
                self.__logged_in = True
                return True
            else:
                print("You don't have enough funds to use a scooter,\nplease add more funds using the website.")
                return False
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return False
        
    def unlock(self):
        self.__status = "Unlocked"
        
    def lock(self):
        self.__status = "Locked"
        
    def logout_timer(self):
        """
        Timer to automatically logout the user when the booking period ends.
        Runs in a separate thread and checks the current time every second.
        If the current time is greater than the end time of the booking, the user and scooter are logged out.
        """
        while self.__logged_in:
            if self.__start_time is not None and self.__end_time is not None:
                current_time = datetime.now(AEST)
                if current_time >= self.__end_time:
                    self.logout()
                    self.__scooter_handler.logout()
            time.sleep(1)
        
    def get_booking_id(self):
        return self.__booking_id
        
    def get_email(self) -> str:
        return self.__email
    
    def get_funds(self) -> float:
        return self.__funds
    
    def get_logged_in(self) -> bool:
        return self.__logged_in
    
    def get_status (self) -> str:
        return self.__status
    
    def get_hash(self) -> str:
        return self.__hash
        
    def logout(self):
        AEST = pytz.timezone('Australia/Sydney')
        print("Logging out...")
        self.__scooter_handler.logout()
        self.__sock.end_booking(self.__booking_id)
        self.__email = None
        self.__logged_in = False
        self.__status = "Locked"
        self.__funds = 0.0
        self.__phone_no = None
        
        
    def parse_iso8601(self, dt_string):
        """
        Converts times to AEST from the DB
        """
        try:
            dt = parser.parse(dt_string)
            dt_aest = dt.astimezone(AEST)
            return dt_aest
        except Exception as e:
            print(f"Error parsing ISO 8601 datetime: {e}")
            return None