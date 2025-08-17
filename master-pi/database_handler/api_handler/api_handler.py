from flask import Flask
from .user_api_handler import UserAPI
from .booking_api_handler import BookingAPI
from .transaction_api_handler import TransactionAPI
from .scooter_api_handler import ScooterAPI
from .faultlog_api_handler import FaultLogAPI


class APIHandler:
    def __init__(self, db_info_file):
        self.app = Flask(__name__)
        self.db_info_file = db_info_file
        # Initialize handler classes with the same db_info_file
        self.user_handler = UserAPI(self.app, db_info_file)
        self.booking_handler = BookingAPI(self.app, db_info_file)
        self.transaction_handler = TransactionAPI(self.app, db_info_file)
        self.scooter_handler = ScooterAPI(self.app, db_info_file)
        self.faullog_handler = FaultLogAPI(self.app, db_info_file)
