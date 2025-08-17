import socket
import json
import struct
from datetime import datetime

class socket_handler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(socket_handler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialised'):
            with open("resources.json", "r") as file:
                data = json.load(file)
                self.HOST = data["master-pi-IP"]
                self.PORT = data["master-pi-PORT"]
            self.ADDRESS = (self.HOST, self.PORT)
            self.connected = False
            self.initialised = True
        
    def send_request(self, command: str, payload: dict):
        """
        Send a request to the server with a given command and payload.

        The message is sent as a JSON string, with the length of the message
        sent first as a 4-byte big-endian integer.

        Args:
            command: The command to send to the server.
            payload: The payload to send with the command.

        Returns:
            The response from the server, or None if there was an error.
        """
        message = {
            "command": command,
            "payload": payload
        }
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.ADDRESS)
                self.connected = True
                json_message = json.dumps(message).encode('utf-8')
                message_length = len(json_message)
                
                # Send the length of the message first (4 bytes, big-endian)
                s.sendall(struct.pack('>I', message_length))
                # Then send the actual message
                s.sendall(json_message)
                
                # Receive response from server
                response_length_data = self._recv_exactly(s, 4)
                if response_length_data is None:
                    # print("Failed to receive response length.")
                    return None
                
                response_length = struct.unpack('>I', response_length_data)[0]
                response = self._recv_exactly(s, response_length)
                
                if response is None:
                    print("Failed to receive full response.")
                    return None

                return response.decode()
        except socket.error as e:
            print(f"{e}")
            self.connected = False
            return None
    
    def _recv_exactly(self, sock, length: int):
        """Helper function to ensure that exactly `length` bytes are read from the socket."""
        data = b''
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                return None  # Connection closed or error
            data += packet
        return data
        
    def get_user_hash(self, email: str) -> str:
        """
        Get the hashed password for a given email from the Database.

        :param email: The email to get the hash for
        :return: The hashed password for the given email if the server returns a valid response, otherwise None
        """
        
        payload = { "email": email }
        response = self.send_request("GLD", payload)
        response = json.loads(response)
        
        if isinstance(response, str):
            return response
        
        if response.get("password") is None:
            return None
        
        user_hash = response.get("password")
        return user_hash
    
    def get_customer_details(self, email: str) -> str:
        payload = { "email": email}
        return self.send_request("GCD", payload)
    
    def get_booking_id(self, email, scooter_num):
        payload = {"email": email, "scooter_id": scooter_num}
        return self.send_request("GBI", payload)
    
    def get_booking_details(self, booking_id):
        payload = {"booking_id": booking_id}
        return self.send_request("GBD", payload)
    
    def start_booking(self, email, booking_id, scooter_id, time):
        payload = {"email": email, "booking_id": booking_id, "scooter_id": scooter_id, "actual_start_datetime": time.isoformat()}
        return self.send_request("SB", payload)
    
    def end_booking(self, booking_id):
        payload = {"booking_id": booking_id}
        return self.send_request("EB", payload)
    
    def get_scooter_info(self, scooterNum: str):
        """
        Get the scooter info for a given scooter number.

        :param scooterNum: The number of the scooter to get info for
        :return: The response from the server if the request is successful, otherwise None
        """
        payload = { "scooter_id": scooterNum}
        return self.send_request("GSD", payload)
    
    def set_scooter_status(self, status: str, scooterNum: str):
        """
        Set the status of a scooter on the Database.

        :param status: The new status for the scooter
        :param scooterNum: The number of the scooter to update
        :return: The response from the server if the request is successful, otherwise None
        """
        payload = { "scooter_id": scooterNum, "status": status }
        return self.send_request("USS", payload)

    def report_scooter_fault(self, scooterNum: str, fault: str):
        payload = {"scooter_id": scooterNum, "fault_notes": fault}
        return self.send_request("RSF", payload)
    
    def set_scooter_ip(self, scooterNum: str):
        ip = self.get_ip()
        if ip == '':
            print("Scooter IP not found")
            return None
        
        payload = {"scooter_id": scooterNum, "scooter_ip": ip}
        return self.send_request("USI", payload)
    
    def update_scooter_location(self, scooterNum: str, lat: float, long: float):
        payload = {"scooter_id": scooterNum, "latitude": lat, "longitude": long}
        return self.send_request("USL", payload)
    
    def create_transaction(self, email, amount, time):
        payload = {"email": email, "transaction_amount": amount, "transaction_datetime": time.isoformat()}
        print("Adding new transaction...")
        return self.send_request("ANT", payload)
    
    def add_booking(self, payload):
        return self.send_request("AB", payload)
    
    def get_ip(self):
        """
        Get the IP address of the device.

        This function creates a socket and attempts to connect to 10.255.255.255
        on port 1. The IP address of the device is then retrieved using
        getsockname()[0] and returned. If the connection fails, an empty string
        is returned. The socket is always closed in the finally block.

        :return: The IP address of the device or an empty string if the connection fails
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = ''
        finally:
            s.close()
        return IP
    
