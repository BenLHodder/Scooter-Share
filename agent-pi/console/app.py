import hashlib
import threading
import time
import os
import pwinput
from pyzbar.pyzbar import decode
from PIL import Image
import json

from utility.input_validation import validate_input, validate_email
from utility.encryption import compare_password

def run(socket, sense, user, scooter, accel_logger):
    """Loop infinitely."""

    while True:
        if not socket.connected:
            scooter.set_status("Needs Repair")

        scooter_status = scooter.get_status()
        sense.display_status(scooter_status)
        # print(scooter_status)
        # time.sleep(5)
        if scooter_status in ["repairing", "Needs Repair"]:
            handle_unavailable_scooter(sense, scooter)
        elif not user.get_logged_in():
            handle_not_logged_in(socket, user, scooter, sense)
        else:
            handle_logged_in(user, scooter, sense, accel_logger, socket)
        

def login():
    """
    Asks the user for their email and password, validating the input for both before returning the valid credentials.
    
    :return: A tuple containing the valid email and password
    """
    clear_terminal()
    valid = False
    while not valid:
        email = input("Enter email: ")
        valid_email = validate_email(email)

        if valid_email:
            password = pwinput.pwinput(prompt="Enter your password: ", mask='*')
            valid_password = validate_input(password)

            if valid_password:
                valid = True
            else: 
                print("Invalid password, please try again.")
        else:
            print("Invalid email, please try again.")
    
    return email, password

    
def handle_unavailable_scooter(sense, scooter):
    message_shown = False
    while scooter.get_status() in ["Repairing", "Needs Repair"]:
        if scooter.get_status() == "Repairing":
            sense.display_status("Needs Repair")
        else:
            sense.display_status("Repairing")
            
        if not message_shown:
            clear_terminal()
            print("Sorry, this scooter is unavailable...")
            message_shown = True
    
    return


def handle_not_logged_in(socket, user, scooter, sense):
    clear_terminal()
    while True:
        if scooter.get_status() in ["Repairing", "Needs Repair"]:
            handle_unavailable_scooter(sense, scooter)
        
        print("1. Log in to the scooter")
        print("2. Report a fault with the scooter")
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            login_user(socket, user, scooter)
            break  # Exit the loop after login
        elif user_choice == "2":
            report_fault(scooter, sense)
            break  # Exit the loop after reporting fault
        else:
            print("Invalid choice, please try again.")

    return False

def login_user(socket, user, scooter):
    clear_terminal()
    valid_choice = False
    using_qr_code = False
    while not valid_choice:
        print("1. Login using password")
        print("2. Login using QR code")
        print("3. Cancel")
        input_choice = input("Enter your choice: ")
        if input_choice == "1":
            email, password = login()
            valid_choice = True
        elif input_choice == "2":
            email, password = get_details_from_qr_code()
            using_qr_code = True
            valid_choice = True
        elif input_choice == "3":
            return
        else:
            print("Invalid choice, Please try again.")
            
    
    # email, password = login()
    user_hash = socket.get_user_hash(email)

    if user_hash is None:
        print("Invalid email or password.")
        print("If you don't have an account, please register on the website.")
        return
    
    
    if compare_password(password, user_hash) and not using_qr_code:
        clear_terminal()
        if scooter.get_status() == "Available":
            print("Logging in...")
            if user.login(email, user_hash, scooter.get_scooter_num()):
                print(email)
                scooter.login(email, user.get_booking_id())
            else:
                print("Scooter has been booked by another user.")
        else:
            print("Scooter is out of service.")
    elif using_qr_code and password == user_hash:
        clear_terminal()
        if scooter.get_status() == "Available":
            print("Logging in...")
            if user.login(email, user_hash, scooter.get_scooter_num()):
                print(email)
                scooter.login(email, user.get_booking_id())
            else:
                print("Scooter has been booked by another user.")
        else:
            print("Scooter is out of service.")
    else:
        print("Invalid credentials.")
    time.sleep(2)


def get_details_from_qr_code():
    clear_terminal()
    valid = False
    while not valid:
        email = input("Enter email: ")
        valid_email = validate_email(email)
        
        if valid_email:
            valid = True
        else:
            print("Invalid email, please try again.")
            
    if email.endswith("@engineer.com"):
        # Hash both email and password for engineers
        email = hashlib.sha256(email.encode()).hexdigest()
    
    filename = f"{email}.png"
    file_path = os.path.join("static/qr-codes", filename)
    
    if os.path.isfile(file_path):
        
        # Try decoding the QR code
        img = Image.open(file_path)  # Open the image file
        decoded_objects = decode(img)  # Decode the QR code

        if decoded_objects:
            # If decoding is successful, process the decoded data
            for obj in decoded_objects:
                data_str = obj.data.decode('utf-8')  # Decoded data as string
                # Parse the JSON string into a Python dictionary
                try:
                    data = json.loads(data_str)  # Convert JSON string to dict
                    return data.get('username'), data.get('password')  # Return relevant fields
                except json.JSONDecodeError:
                    print("Failed to decode the QR code JSON data.")
                    return None, None
        else:
            print("No QR code found or decoding failed.")
            return None, None
    else:
        print("QR code file not found.")
        return None, None
        

def report_fault(scooter, sense):
    # clear_terminal()
    if scooter.get_status() in ["Repairing", "Needs Repair"]:
        handle_unavailable_scooter(sense, scooter)
        
    print("Type 'cancel' to stop reporting a fault.")
    fault = input("Enter your fault here: ")
    if fault.lower() == "cancel":
        print("Fault reporting cancelled.")
    else:
        scooter.report_fault(fault)
        scooter.set_status("Needs Repair")
        print("Fault reported successfully.")
        handle_unavailable_scooter(sense, scooter)

def handle_logged_in(user, scooter, sense, accel_logger, socket):
    while True:
        if scooter.get_status() in ["Repairing", "Needs Repair"]:
            handle_unavailable_scooter(sense, scooter)
        
        accel_logger.start_timer(100)
        clear_terminal()
        print("1. Unlock scooter")
        print("2. Log out")
        print("3. Report a fault with the scooter")
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            unlock(user, scooter, sense)
        elif user_choice == "2":
            accel_logger.stop_timer()
            max_x, max_y, max_z = accel_logger.find_largest_acceleration("acceleration_data.csv")
            max_value = max(max_x, max_y, max_z)
            to_kmph = max_value * 9.81 * 3.6
            print(f"Your top acceleration was: {to_kmph:.2f}km/h")
            print("Press enter to continue logging out...")
            input()
            
            user.logout()
            scooter.logout()
            sense.display_status("Available")
            handle_not_logged_in(socket, user, scooter, sense)
        elif user_choice == "3":
            report_fault(scooter, sense)
            break
        else:
            print("Invalid choice, please try again.")

def unlock(user, scooter, sense):
    while True:
        if scooter.get_status() in ["Repairing", "Needs Repair"]:
            handle_unavailable_scooter(sense, scooter)
        
        clear_terminal()
        password = pwinput.pwinput(prompt="Enter your password: ", mask='*')
        if compare_password(password, user.get_hash()):
            clear_terminal()
            print("Unlocked...")
            user.unlock()
            while True:  # loop until user decides to lock or report a fault
                user_choice = input("1. Lock scooter\n2. Report a fault with the scooter\nEnter your choice: ")
                if user_choice == "1":
                    print("Locking...")
                    user.lock()
                    break  # Exit the loop after locking
                elif user_choice == "2":
                    report_fault(scooter, sense)
                else:
                    print("Invalid choice, please try again.")
            break
        else:
            clear_terminal()
            print("Invalid password.")
            print("Press enter to continue...")
            input()
        
def clear_terminal():
    """
    Clears the terminal screen.
    """
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux (here, 'posix' is a common value for these)
    else:
        os.system('clear')