from email import parser
import socket
import json
import struct
import threading
import time
from datetime import datetime, timedelta
from dateutil import parser
import pytz
from threading import Timer
from .API_handler import api_handler
from datetime import datetime
from utils.email_sender import EmailSender
from model.booking import Booking

AEST = pytz.timezone('Australia/Sydney')

class socket_handler:
    def __init__(self):
        self.AGENT_PI_IP = None
        self.AGENT_PI_PORT = 65001
        self.host = ""
        self.port = 65000
        self.ADDRESS = (self.host, self.port)
        self.previous_statuses = {}
        self.local_tz = pytz.timezone('Australia/Sydney')
        
        # Start checking for bookings when the class is initialized
        self.check_active_bookings()
        
        # Start a thread to update scooter statuses
        
        t_update_scooter_status = threading.Thread(target=self.update_scooter_status_thread, args=(api_handler(),))
        t_update_scooter_status.daemon = True
        t_update_scooter_status.start()
        
        # Set a timer to run the check every hour
        self.schedule_booking_check()
        api = api_handler()

        self.start_listening(api)

    def start_listening(self, api):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            s.listen()
            print("Listening on {}...".format(self.ADDRESS))

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")

                    try:
                        # First, receive the length of the incoming message (4 bytes, big-endian)
                        raw_msglen = self.recv_all(conn, 4)
                        if not raw_msglen:
                            return
                        msglen = struct.unpack(">I", raw_msglen)[0]

                        # Now, receive the actual message based on the length
                        received_data = self.recv_all(conn, msglen)
                        if not received_data:
                            return

                        # Decode the received bytes into a string
                        message_str = received_data.decode()
                        print(f"Received message: {message_str}")

                        # Deserialize the JSON string to a Python dictionary
                        message = json.loads(message_str)

                        # Handle the command and payload
                        command = message.get("command")
                        payload = message.get("payload")

                        response_str = self.command_handler(command, payload, api)
                        response_bytes = response_str.encode()
                        # Send the response length and the response itself
                        conn.sendall(struct.pack(">I", len(response_bytes)))
                        conn.sendall(response_bytes)

                    except json.JSONDecodeError:
                        print("Failed to decode JSON message from client.")

                    print("Disconnecting from client.")
        print("Done.")
        
    def update_scooter_status_thread(self, api):
        
        """
        Periodically polls the API for scooter status updates and sends the updated status to the agent.

        Args:
            api (APIInterface): The APIInterface instance to use for getting scooter status updates.

        Returns:
            None
        """
       
        while True:
            scooter_response = api.get_all_scooters()
            booking_response = api.get_all_bookings_for_scooters().get('all_booked_scooters', [])
            current_time = datetime.now(AEST)

            # Updating scooter status on AP if status has changed
            for scooter in scooter_response:
                scooter_id = scooter["scooterID"]
                status = scooter["status"]
                
                if scooter_id not in self.previous_statuses:
                    self.previous_statuses[scooter_id] = status
                elif self.previous_statuses[scooter_id] != status:
                    print(f"Scooter {scooter_id} changed status from {self.previous_statuses[scooter_id]} to {status}.")
                    self.previous_statuses[scooter_id] = status
                    self.send_request_to_agent(scooter["ipAddress"], "USS", {"status": status})
                
                for booking in booking_response:
                    if isinstance(booking, dict) and "scooterID" in booking:
                        if booking.get("status") == "Active" and booking.get("scooterID") == scooter_id and status == "Available":
                            # print(f"Booking Status: {booking.get("status")}")
                            start_time = self.parse_iso8601(booking.get("startDateTime"))
                            end_time = self.parse_iso8601(booking.get("endDateTime"))
                            if start_time - timedelta(minutes=10) <= current_time< start_time:
                                print(current_time + timedelta(minutes=10))
                                print(f"Booking: {booking}")
                                print("10 minutes before start time")
                                scooter_data = {"scooter_id": scooter_id, "status": "Booked"}
                                api.set_scooter_status(scooter_data)
                                self.send_request_to_agent(scooter["ipAddress"], "USS", {"status": "Booked"})

                            # Check if current time is between start_time and end_time
                            elif start_time < current_time < end_time:
                                print(f"Booking: {booking}")
                                print("In between start and end time")
                                scooter_data = {"scooter_id": scooter_id, "status": "Booked"}
                                self.previous_statuses[scooter_id] = "Booked"
                                api.set_scooter_status(scooter_data)
                                self.send_request_to_agent(scooter["ipAddress"], "USS", {"status": "Booked"})
                            # Otherwise check if the time is after or before the start or end
                            else:
                                if current_time < start_time:
                                    print("Before start time")
                                elif current_time > end_time:
                                    print("After end time")
                                else:
                                    print("Error in time comparison")
            time.sleep(5)

  
    def send_request_to_agent(self, ip: str, command: str, payload: dict):
        """
        Send a request to the Agent Pi at the given IP address.
        
        :param ip: The IP address of the Agent Pi to send the request to.
        :param command: The command to send to the Agent Pi.
        :param payload: The payload to send to the Agent Pi.
        :return: The response from the Agent Pi as a string, or None if the request failed.
        """
        
        self.AGENT_PI_IP = ip
        message = {
            "command": command,
            "payload": payload
        }

        agent_address = (self.AGENT_PI_IP, self.AGENT_PI_PORT)
        print(f"Sending request to Agent Pi at {agent_address}: {message}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(agent_address)
                json_message = json.dumps(message).encode('utf-8')
                message_length = len(json_message)
                
                # Send the length of the message first (4 bytes, big-endian)
                s.sendall(struct.pack('>I', message_length))
                # Then send the actual message
                s.sendall(json_message)
                
                # Receive response from Agent Pi
                response_length_data = self._recv_exactly(s, 4)
                if response_length_data is None:
                    print("Failed to receive response length.")
                    self.AGENT_PI_IP = None
                    return None
                
                response_length = struct.unpack('>I', response_length_data)[0]
                response = self._recv_exactly(s, response_length)
                
                if response is None:
                    print("Failed to receive full response.")
                    self.AGENT_PI_IP = None
                    return None

                self.AGENT_PI_IP = None
                return response.decode()
        except socket.error as e:
            print(f"Can't connect to Agent Pi: {e}")
            self.AGENT_PI_IP = None
            return None
        
    def command_handler(self, command, payload, api):
        """
        Handle commands and payloads from clients.

        Args:
            command (str): Command sent by the client.
            payload (dict): Payload sent by the client.

        Returns:
            str: JSON response containing the result of the command.
        """
        
        ###
        # Booking API
        ###            
        if command == "CB": #Cancel booking
            print(f"Cancel booking requested for user: {payload['booking_id']}")
            response = api.cancel_booking(booking_id=payload['booking_id'])
            
            return json.dumps(response)
                
        elif command == "AB": #Add booking
            print("Add booking")
            response = api.add_booking(payload)
            
            return json.dumps(response)
            
        elif command == "GBD": #Get booking details
            print(f"Get booking details requested for user: {payload['booking_id']}")
            response = api.get_booking(booking_id=payload['booking_id'])
            
            return json.dumps(response)
        
        
        elif command == "SB":  # Start booking
            print(f"Start booking requested for booking id: {payload['booking_id']}")
            response = api.get_booking(booking_id=payload['booking_id'])
            print(f"get booking response {response}")
            # Parse the date strings into datetime objects
            try:
                booking_start = self.parse_iso8601(response.get("startDateTime"))
                booking_end = self.parse_iso8601(response.get("endDateTime"))
                # booking_start = AEST.localize(booking_start)
                # booking_end = AEST.localize(booking_end)
                actual_start = datetime.now(AEST)
                print("done with times")
            except ValueError:
                print("Invalid datetime format")
                return json.dumps({"error": "Invalid datetime format"})
            
            print(f"Actual start: {actual_start}")
            print(f"Booking start: {booking_start}")
            print(f"Booking end: {booking_end}")
            
            # Check if the email or scooterID don't match or if the start time is outside the booking window
            if (response.get("email") != payload.get("email") or 
                str(response.get("scooterID")) != str(payload.get("scooter_id")) or 
                not (booking_start <= actual_start <= booking_end)):
                    print("Booking does not match user")
                    return json.dumps({"error": "Booking does not match user"})
            
            # Start the booking process
            start_booking_payload = {"booking_id": payload['booking_id'], "actual_start_datetime": actual_start.isoformat()}
            print(start_booking_payload)
            response = api.start_booking(start_booking_payload)
            print(response)
            api.set_scooter_status({"scooter_id": payload['scooter_id'], "scooter_status": "In Use"})
            
            return json.dumps(response)
        
        
        elif command == "EB": #End booking
            print(f"End booking requested for booking id: {payload['booking_id']}")
            response = api.get_booking(booking_id=payload['booking_id'])
            
            try:
                print(response)
                actual_start = self.parse_iso8601(response.get("actualStartDateTime"))
                actual_end = datetime.now(AEST)
            except ValueError:
                print("Invalid datetime format")
                return json.dumps({"error": "Invalid datetime format"})
            
            # if (response.get("email") != payload.get("email") or 
            #     str(response.get("scooterID")) != str(payload.get("scooter_id"))):
            #         print("Booking does not match user")
            #         return json.dumps({"error": "Booking does not match user"})
            
            print(f"Payload: {payload}")
            scooter_data = api.get_scooter_details(response.get("scooterID"))
            costMinute = scooter_data.get("costMin")
            time_difference = (actual_end - actual_start).total_seconds() / 60
            total_cost = round(time_difference * costMinute, 2)
            
            transaction_payload = {"email": response.get("email"), "transaction_amount": total_cost, "transaction_datetime": datetime.now(AEST).isoformat()}
            transaction = api.add_transaction(transaction_payload)
            
            customer = api.get_customer_details(response.get("email"))
            customer_funds = customer.get("funds")
            
            new_customer_funds = customer_funds - total_cost
            new_funds_payload = {"email": response.get("email"), "funds": new_customer_funds}
            new_funds_response = api.update_customer_funds(new_funds_payload)
            
            if new_funds_response.get("message") != "Customer funds updated successfully.":
                print(new_funds_response)
                return json.dumps(new_funds_response)
            
            if transaction.get("message") == "Transaction added successfully.":
                end_booking_payload = {"booking_id": payload['booking_id'], "actual_end_datetime": actual_end.isoformat()}
                response = api.end_booking(end_booking_payload)
                print(f"HERE {response}")
                response = api.set_booking_status_complete(payload['booking_id'])
                print(f"HERE1 {response}")
                api.set_scooter_status({"scooter_id": response.get("scooterID"), "scooter_status": "Available"})
                self.previous_statuses[response.get("scooterID")] = "Available"
                
            
            return json.dumps(response)
        
        
        elif command =="GAB": #Get all bookings
            print(f"Get all bookings requested for user: {payload['email']}")
            response = api.get_all_bookings(email=payload['email'])
            
            return json.dumps(response)
        
        elif command == "GABS": #Get all booked scooter times
            print("Get all booked scooter times")
            response = api.get_all_bookings_for_scooters()
            
            return json.dumps(response)
        
        elif command == "GBI": #Get booking ID
            print(f"Get booking ID requested for user: {payload['email']}")
            data = api.get_all_bookings(email=payload['email'])
            data_list = data.get("bookings", [])
            response = []
            print(data)
            for booking in data_list:
                start_time = self.parse_iso8601(booking.get("startDateTime"))
                end_time = self.parse_iso8601(booking.get("endDateTime"))
                current_time = AEST.localize(datetime.now())
                print(f"curr: {current_time}")
                print(f"start: {start_time}")
                print(f"end: {end_time}")
                print(start_time <= current_time <= end_time)
                print(booking.get("scooterID"))
                print(payload.get("scooter_id"))
                print(booking.get("status"))
                print(booking)
                print(payload)
                booking_scooter = booking.get("scooterID")
                payload_scooter = payload.get("scooter_id")
                print(f"booking_scooter: {booking_scooter}")
                print(f"payload_scooter: {payload_scooter}")
                print("############")
                
                if (str(booking_scooter) == str(payload_scooter)):
                    print("Step 1")
                    if (booking.get("status") == "Active"):
                        print("Step 2")
                        if (start_time <= current_time <= end_time):
                            print("Step 3")
                            print("Adding booking")
                            response.append(booking.get("bookingID"))
                            print("Added booking")
            
            if len(response) == 0:
                return json.dumps({"error": "No booking found"})
            elif len(response) == 1:
                print(response)
                return json.dumps({"bookingID": response[0]})
            else:
                return json.dumps({"error": "Multiple bookings found"})

        elif command == "SBG": # Set booking google ID
            print(f"Updating booking Google ID for booking: {payload['booking_id']}")
            response = api.set_booking_googleID(payload.get("booking_id"), payload.get("google_id"))
            return json.dumps(response)
        
        elif command == "GABFS": #Get all bookings for a scooter
            print(f"Get all bookings for a scooter: {payload['scooter_id']}")
            response = api.get_all_bookings_for_scooter(payload.get("scooter_id"))
            
            return json.dumps(response)
            
        ###
        # Customer API
        ###          
        elif command == "GCD": #Get customer details
            print(f"Get customer details requested for user: {payload['email']}")
            response = api.get_customer_details(email=payload['email'])
            
            return json.dumps(response)
            
        elif command == "GLD": # Get login details
            print(f"Getting login details requested for user: {payload['email']}")
            customer_details = api.get_customer_details(email=payload['email'])
            customer_password = api.get_login_details(email=payload['email'])
            # Wrap the response into a dict or object
            details = {
                "email": customer_details.get("email"),
                "password": customer_password.get("password"),
                "role": customer_details.get("role"),
            }
            
            return json.dumps(details)
        
        elif command == "RNC": #register new customer
            print(f"Add customer requested for user: {payload['email']}")
            response = api.register_new_customer(payload)
            
            return json.dumps(response)
        
        elif command == "DC": #Delete customer
            print(f"Delete customer requested for user: {payload['email']}")
            response = api.delete_customer(email=payload['email'])
            
            return json.dumps(response)
        
        elif command == "UCF": #Update customer funds
            print(f"Update customer funds requested for user: {payload['email']}")
            response = api.update_customer_funds(payload)
            
            return json.dumps(response)
        
        elif command == "GAC": #Get all customers
            print("Get all customers")
            response = api.get_all_customers()
            
            return json.dumps(response)
        
        elif command == "UCD": #Update customer details
            print(f"Update customer details requested for user: {payload['email']}")
            response = api.update_customer_details(payload['email'], payload)
            
            return json.dumps(response)
        
        elif command == "FP": #Forgot password
            print(f"Forgot password requested for user: {payload['email']}")
            body = f"Click the link below to reset your password:\n{payload['url']}"
            rec = ["group12.cosc2674@gmail.com", payload['email']]
            EmailSender.send_email("backend/resources/smtp_details.json", rec, "Reset Password", body)
            
            return json.dumps({"message": "success"})
        
        ###
        # Scooter API
        ###            
        elif command == "GSD": #Get scooter details
                print(f"Get scooter details requested for scooter: {payload['scooter_id']}")
                response = api.get_scooter_details(scooter_id=payload['scooter_id'])
                
                return json.dumps(response)
            
        elif command == "USS": #Set scooter state
            print(f"Set scooter state requested for user: {payload['scooter_id']}")
            response = api.set_scooter_status(payload)
            
            return json.dumps(response)
        
        elif command == "RSF": #Report scooter fault
            print(f"Report scooter fault requested for scooter: {payload['scooter_id']}")
            status_payload = {"scooter_id":payload['scooter_id'], "status": "Needs Repair"}
            api.set_scooter_status(status_payload)
            response = api.update_scooter_fault(payload)
            fault_response = api.get_fault_by_scooter(payload['scooter_id']) 
            
            if fault_response and isinstance(fault_response, list) and isinstance(fault_response[0], list):
                fault_data = fault_response[0]  # Access the inner list

                # Extract details using indices
                fault_id = fault_data[0]
                fault_notes = fault_data[6] 
                start_date_time = fault_data[2]   
                status = fault_data[4]            

                # Construct the body
                body = (
                    f"""Your scooter {payload['scooter_id']} has been reported as a fault. 
                    Fault details: 
                    \nFault ID: {fault_id} 
                    \nFault Notes: {fault_notes} 
                    \nReported at: {start_date_time} 
                    \nStatus: {status}"""
                )
            else:
                body = f"Scooter {payload['scooter_id']} has been reported as a fault. No fault details found."
                
            # Send email to engineers
            recipients = api.get_all_engineer_emails()
            
            # checking if email has valid format
            rec = ['group12.cosc2674@gmail.com']
            for recipient in recipients:
                if '@' in recipient:
                    rec.append(recipient)
            EmailSender.send_email("backend/resources/smtp_details.json", rec, f"Scooter {payload['scooter_id']} Fault Reported {start_date_time}", body)
            
            return json.dumps(response)
        
        elif command == "GAS": #Get all scooters
            print("Get all scooters")
            response = api.get_all_scooters()
            
            return json.dumps(response)
        
        elif command == "USL": #Update scooter location
            print(f"Update scooter location requested for scooter: {payload['scooter_id']}")
            new_payload = {"latitude": payload['latitude'], "longitude": payload['longitude']}
            response = api.update_scooter_location(payload['scooter_id'], new_payload)
            
            return json.dumps(response)
        
        elif command == "USI": #Update scooter ip
            print(f"Update scooter ip requested for scooter: {payload['scooter_id']}")
            new_payload = {"ip_address": payload['scooter_ip']}
            response = api.update_scooter_ip_address(payload['scooter_id'], new_payload)
            
            return json.dumps(response)
        
        elif command == "FMS": #Find my scooter
            print(f"Find my scooter requested for scooter: {payload['scooter_id']}")
            response = api.get_scooter_details(scooter_id=payload['scooter_id'])
            scooter_ip = response.get("ipAddress")
            print(self.send_request_to_agent(scooter_ip, "FMS", {"ip_address": scooter_ip}))
            
            return json.dumps({"success": True})
            
        elif command == "USD": #Update scooter details
            print(f"Update scooter details requested for scooter: {payload['scooter_id']}")
            response = api.update_scooter_details(payload['scooter_id'], payload)
            
            return json.dumps(response)
        
        ###
        # Transaction API
        ###
        elif command == "GTD": #Get transaction details
            print(f"Get transaction details requested for transaction: {payload['transaction_id']}")
            response = api.get_transaction(transaction_id=payload['transaction_id'])
            
            return json.dumps(response)
        
        elif command == "ANT": #Add new transaction
            print("Add new transaction")
            response = api.add_transaction(payload)
            
            return json.dumps(response)
        
        elif command == "GACT": #Get all customer transactions
            print (f"Get all customer transactions requested for user: {payload['email']}")
            response = api.get_customer_transactions(customer_id=payload['email'])
            
            return json.dumps(response)
        

        ###
        # Fault Log API
        ###
        elif command == "GFBI": # Get fault by id
            print(f"Get fault by id: {payload['fault_id']}")
            response = api.get_fault_by_id(payload['fault_id'])
            
            return json.dumps(response)
        
        elif command == "GOF": #Get open faults
            print("Get open faults")
            response = api.get_open_faults()
            
            return json.dumps(response)
        
        elif command == "GFBS": #Get fault by scooter id
            print(f"Get fault by scooter id: {payload['scooter_id']}")
            response = api.get_fault_by_scooter(payload['scooter_id'])
            
            return json.dumps(response)
        
        elif command == "USF": #Update scooter fault
            print(f"Update scooter fault requested for scooter: {payload['scooter_id']}")
            response = api.update_scooter_fault(payload)
            
            return json.dumps(response)
        
        elif command == "RESF": #Resolve scooter fault
            print(f"Resolve scooter fault requested for scooter: {payload['fault_id']}")
            response = api.resolve_scooter_fault(payload['fault_id'], payload)

            fault_response = api.get_fault_by_id(payload['fault_id'])
            
            scooter_id = fault_response.get('scooterID')
            status_payload = {"scooter_id": scooter_id, "status": "Available"}
            print(f"Updating scooter status: {status_payload}")
            api.set_scooter_status(status_payload)
        
            return json.dumps(response)
        
        ###
        # Default
        ###
        else:
            print(f"Unknown command: {command}")
            return json.dumps({"error": "Unknown command"})
            

    def recv_all(self, conn, length):
        """
        Receive all of the data from a socket, given a length.

        :param conn: The socket connection to receive from.
        :param length: The number of bytes to receive.
        :return: The received data as a bytes object, or None if a zero-length packet is received.
        """
        data = b""
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data
    
    def _recv_exactly(self, sock, length: int):
        """Helper function to ensure that exactly `length` bytes are read from the socket."""
        data = b''
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                return None  # Connection closed or error
            data += packet
        return data
    
    def check_active_bookings(self):
        """
        Check for active bookings and mark them as 'complete' if their endDateTime has elapsed.
        """
        api = api_handler()
        print("Checking for active bookings...")
        
        # Get all active bookings from the API
        active_bookings = api.get_active_bookings()
        for booking_data in active_bookings.get('active_bookings', []):
            booking = Booking.from_dict(booking_data)
            # Convert booking's endDateTime to a UTC datetime object
            if booking.endDateTime:
                utc = pytz.utc
                end_datetime_utc = utc.localize(datetime.strptime(booking.endDateTime, '%a, %d %b %Y %H:%M:%S %Z'))
                # Convert UTC to local timezone
                end_datetime_local = end_datetime_utc.astimezone(self.local_tz)
                # Compare the converted local time with the current local time
                if datetime.now(self.local_tz) > end_datetime_local and booking.status != 'Complete':
                    print(f"Booking {booking.bookingID} has elapsed. Marking as complete...")
                    api.set_booking_status_complete(booking.bookingID)
    
    def schedule_booking_check(self):
        """
        Schedule the booking check to run every hour.
        """
        # Schedule this method to run again in one hour (3600 seconds)
        Timer(3600, self.run_booking_check_periodically).start()
    
    def run_booking_check_periodically(self):
        """
        Check for active bookings and reschedule the check to run again in one hour.
        """
        self.check_active_bookings()
        self.schedule_booking_check()
        
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