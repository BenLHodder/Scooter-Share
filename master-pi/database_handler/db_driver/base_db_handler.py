import logging
import pytz
from db_driver.database_driver import DatabaseDriver
from datetime import datetime

class BaseHandler:
    def __init__(self, db_info):
        """
        Initialize the BaseHandler with the specified database info file.
        """
        self._db_info = db_info
        self._db_driver = DatabaseDriver(db_info)
        self._setup_logging()

    def _setup_logging(self):
        """
        Set up logging configuration for the class.
        """
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
    
    def _to_aest(self, dt):
        """Convert naive or UTC datetime to Australia/Sydney timezone."""
        # If dt is a string, attempt to convert it to a datetime object
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)  # Example for ISO format
        
        aest_tz = pytz.timezone('Australia/Sydney')
        if dt.tzinfo is None:  # If naive datetime
            dt = aest_tz.localize(dt)  # Localize to AEST
        else:  # If timezone-aware datetime
            dt = dt.astimezone(aest_tz)  # Convert to AEST
        return dt