from sense_hat import SenseHat
from handlers.audio_handler import audio_handler
import datetime

class sense_handler:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        
        if not cls._instance:
            cls._instance = super(sense_handler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialised'):
            self.sense = SenseHat()
            self.audio = audio_handler()
            self.initialised = True
        
    def display_status(self, status: str) -> None:
        """
        Displays a status on the Sense Hat display.
        
        :param status: A string indicating the status to be displayed. 
        Options are "Available", "booked", "occupied", or "repairing". 
        If the status is not one of these, the scooter is assumed to be broken and the repair logo is displayed.
        """
        # print(f"Status: {status}")
        if status == "Find Me":
            self.display_blinking()
        elif status == "Available":
            self.sense.show_letter("F", back_colour=[0, 255, 0])
        elif status == "Booked":
            self.sense.show_letter("B", back_colour=[0, 0, 255])
        elif status == "In Use" or status == "Locked" or status == "Unlocked":
            self.sense.show_letter("O", back_colour=[255, 0, 0])
        elif status == "Repairing":
            self.sense.show_letter("R", text_colour=[255, 255, 0] ,back_colour=[255, 0, 0])            
        else:
            self.sense.set_pixels(self.repair())
        
        
    def display_blinking(self):
        """
        Blinks the Sense Hat display and plays a sound for 10 seconds.

        This method is used to visually and audibly alert the user that the scooter has been found.
        """
        start_time = datetime.datetime.now()
        count = 0
    
        while (datetime.datetime.now() - start_time).seconds < 10:
            if count % 2 == 0:  # Blink and play sound every 2 counts (roughly every second)
                self.sense.show_letter(" ", back_colour=[0, 255, 0])  # Display with green background
                self.audio.play_bell(1)  # Play sound for 1 second
            else:
                self.sense.clear()  # Clear the screen
                self.audio.play_bell(1)  # Play sound for 1 second
                
            count += 1

                
    def repair(self) -> list:
        """
        Displays a logo of a Raspberry Pi on the Sense Hat.
        
        Returns:
            list: A 2D list of RGB values representing the logo.
        """
        r = [255, 0, 0]
        y = [255, 255, 0]
        
        logo = [r, r, y, y, y, r, r, r,
                r, r, r, y, y, y, r, r,
                y, r, r, r, y, y, y, r,
                y, y, r, r, r, y, y, y,
                y, y, y, r, r, r, y, y,
                r, y, y, y, r, r, r, y,
                r, r, y, y, y, r, r, r,
                r, r, r, y, y, y, r, r
                ]
        
        return logo
    
    # Function to get acceleration
    def get_acceleration(self) -> dict:
        """
        Returns the acceleration values in the x, y, and z directions.
        
        Returns:
            dict: A dictionary containing the acceleration values in the x, y, and z directions.
        """
        acceleration = self.sense.get_accelerometer_raw()
        return acceleration
