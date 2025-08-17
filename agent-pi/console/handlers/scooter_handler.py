import time
import json
import pytz
from datetime import datetime, timedelta

AEST = pytz.timezone('Australia/Sydney')

class ScooterState:
    def handle(self, scooter):
        raise NotImplementedError("Subclasses should implement this method.")

    def login(self, scooter, user, booking_id):
        raise NotImplementedError("This action is not allowed in the current state.")

    def logout(self, scooter):
        raise NotImplementedError("This action is not allowed in the current state.")

    def report_fault(self, scooter, fault):
        raise NotImplementedError("This action is not allowed in the current state.")



class AvailableState(ScooterState):
    def handle(self, scooter):
        print("Scooter is now available.")
        scooter.set_status("Available")

    def login(self, scooter, user, booking_id):
        if scooter.battery > 0:
            print(f"{user} logged into the scooter.")
            scooter.set_user(user)
            scooter.set_booking_id(booking_id)
            scooter.set_state(InUseState())
        else:
            print("Scooter battery is too low to log in.")
            
class BookedState(ScooterState):
    def handle(self, scooter):
        print("Scooter is booked.")
        scooter.set_status("Booked")

class InUseState(ScooterState):
    def handle(self, scooter):
        print("Scooter is in use.")
        scooter.set_status("In Use")

    def logout(self, scooter):
        print(f"{scooter.get_user()} logged out from the scooter.")
        scooter.set_user(None)
        scooter.set_state(AvailableState())

class NeedsRepairsState(ScooterState):
    def handle(self, scooter):
        print("Scooter needs repairs.")
        scooter.set_status("Needs Repairs")

    def report_fault(self, scooter, fault):
        print(f"Reported fault: {fault}")


class scooter_handler:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(scooter_handler, cls).__new__(cls)
        return cls._instance
    
    
    def __init__(self, socket, sense_handler):
         if not hasattr(self, 'initialised'):
            with open("resources.json", "r") as file:
                data = json.load(file)
                self.__scooterNum = str(data.get("scooterNum", "4"))  # Fallback to "4" if scooter_id is not found
            self.__status = None
            self.__user = None
            self.__cost = None
            self.__lat = None
            self.__long = None
            self.__start_time = None
            self.__end_time = None
            self.__make = None
            self.__battery = None
            self.__colour = None
            self.__sock = socket
            self.__booking_id = None
            self.__ip = None
            self.initialised = True
            
            # Initial state is Available
            self.state = AvailableState()
            self.__sense = sense_handler
            
            socket.set_scooter_ip(self.__scooterNum)
            self.reload_info()
        
        
    def reload_info(self):
        """
        Reloads the scooter's information from the server.
        
        This includes the scooter's status, make, cost per minute, battery percentage, and colour.
        """
        response = self.__sock.get_scooter_info(self.__scooterNum)
        if response is not None:
            try:
                resp_dict = json.loads(response)
                # Extract information, handling missing keys with default values or error messages
                status = resp_dict.get("status", "unknown")
                make = resp_dict.get("make", "unknown")
                cost_min = resp_dict.get("costMin", 0)
                battery_percentage = resp_dict.get("batteryPercentage", 0)
                colour = resp_dict.get("colour", "unknown")
                # Set the information using the values obtained
                self.set_info(status, make, cost_min, battery_percentage, colour)
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse response as JSON: {e}")
            except KeyError as e:
                print(f"Error: Missing key in response data: {e}")


    def get_status(self):
        """
        Returns the status of the scooter.

        :return: The status of the scooter.
        """
        
        return self.__status
    
    def get_user(self):
        """
        Returns the user associated with the scooter.

        :return: The user associated with the scooter.
        """
        return self.__user
    
    def set_info(self, status, make, costMin, battery, colour):
        """
        Sets the scooter's status, make, cost per minute, battery percentage, and colour.

        :param status: The new status of the scooter.
        :param make: The make of the scooter.
        :param costMin: The cost of the scooter per minute.
        :param battery: The battery percentage of the scooter.
        :param colour: The colour of the scooter.
        """
        self.__status = status
        self.__make = make
        self.__cost = costMin
        self.__battery = battery
        self.__colour = colour

    def set_status(self, status):
        """
        Sets the status of the scooter to the given value, and updates the server.
        
        :param status: The new status of the scooter. Should be one of "free", "in-use", or "maintenance"
        """
        self.__status = status
        self.__sense.display_status(status)
        self.__sock.set_scooter_status(status, self.__scooterNum)
        
    def get_scooter_num(self):
        
        """
        Returns the scooter number of this scooter.
        
        :return: The scooter number as a string
        """
        return self.__scooterNum
    
    def login(self, user, booking_id):
        """
        Logs in a user on this scooter, given that the scooter has enough battery.

        :param user: The email of the user to log in
        :param booking_id: The booking id of the booking to associate with this login
        :return: True if the user was successfully logged in, False if the scooter has no charge left
        """
        if self.__battery is not None and self.__battery > 0:
            self.__user = user
            self.__start_time = datetime.now(AEST)
            self.__booking_id = booking_id
            self.__sock.start_booking(user, booking_id, self.__scooterNum, self.__start_time)
            self.set_status("In Use")
            self.__sense.display_status("In Use")
            return True
        
        print("Battery is out if charge")
        return False
    
    def logout(self):
        """
        Logs out the user on this scooter, stopping the booking and calculating the total cost based on the time used.
        
        :return: The total cost of the booking, or 0.0 if the logout fails
        """
        if self.__start_time is not None and self.__status == "In Use":
            # Calculate total cost based on AEST time difference
            end_time = datetime.now(AEST)
            total_duration_minutes = (end_time - self.__start_time).total_seconds() / 60
            total_cost = 0 - (total_duration_minutes * self.__cost)
            self.__start_time = None
            self.set_status("Available")
            # self.__sock.create_transaction(self.__user, total_cost, end_time)
            return total_cost
        
        print(str(self.__start_time) + " | " + self.__status)
        print("Error")
        return 0.0
    
    def report_fault(self, fault):
        """
        Reports a fault with this scooter to the server.

        :param fault: A description of the fault with the scooter
        """
        self.__sock.report_scooter_fault(self.__scooterNum, fault)
        
    def set_user(self, user):
        """
        Sets the user associated with this scooter.

        :param user: The email of the user to set as associated with this scooter
        """
        self.__user = user

    def get_user(self):
        """
        Gets the user associated with this scooter.

        :return: The email of the user associated with this scooter
        """
        return self.__user


    def set_booking_id(self, booking_id):
        
        """
        Sets the booking id associated with this scooter.

        :param booking_id: The booking id to set
        """
        self.__booking_id = booking_id

    def get_booking_id(self):
        """
        Gets the booking id associated with this scooter.

        :return: The booking id associated with this scooter
        """
        return self.__booking_id
        
        