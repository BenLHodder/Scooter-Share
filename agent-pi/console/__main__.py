import threading
import time
import os

from handlers.socket_handler import socket_handler
from handlers.user_handler import user_handler
from handlers.scooter_handler import scooter_handler
from handlers.sense_handler import sense_handler
from handlers.listener import listener
from handlers.audio_handler import audio_handler
from handlers.accel_logger import AccelLogger
from app import run

def launch():
    """
    Initializes all the handlers and starts the listener thread before calling the main function to handle user input.
    
    :return: None
    """
    sense = sense_handler()
    print("Starting up...")
    
    socket = socket_handler()
    scooter = scooter_handler(socket=socket, sense_handler=sense)
    user = user_handler(socket=socket, scooter_handler=scooter)
    accel_logger = AccelLogger(sense, "acceleration_data.csv")
    
    listener_t = threading.Thread(target=listener_thread, args=(sense, scooter), daemon=True)
    listener_t.start()
    
    status = scooter.get_status()
    print("Setup Complete:")
    print(f"Scooter Status: {status}")
    print(f"Socket Status: {'Connected' if socket.connected else 'Disconnected'}")
    print(f"User Status: {user.get_status()}")
    print(f"Acceleration Logger Status: {accel_logger.running}")
    sense.display_status(status)
    
    print("Press enter to continue...")
    input()
    run(socket, sense, user, scooter, accel_logger)
    
def listener_thread(sense, scooter):
    listener(sense, scooter)
                   
def clear_file(file_path):
    """
    Clear the contents of a file.
    
    :param file_path: The path to the file to clear.
    """
    with open(file_path, 'w') as f:
        f.write('')

if __name__ == "__main__":
    launch()