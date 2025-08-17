import socket
import json
import struct

class listener():
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(listener, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, sense_handler, scooter_handler):
        if not hasattr(self, 'initialised'):
            self.port = 65001
            self.host = ""
            self.ADDRESS = (self.host, self.port)
            self.sense_handler = sense_handler
            self.scooter_handler = scooter_handler
            self.scooter_status = scooter_handler.get_status()
            self.__start_listening()
            self.initialised = True

    def __start_listening(self):
        """
        Starts listening for incoming connections on the specified address and port.
        
        When a connection is received, it will receive a JSON message, decode it, and call the __command_handler
        method with the command and payload. The response from the handler will then be sent back to the client.
        
        This method is called by the constructor, and it will run indefinitely until the program is terminated.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            s.listen()
            print("Listening on {}...".format(self.ADDRESS))
            
            while True:
                conn, addr = s.accept()
                with conn:
                    # print(f"Connected by {addr}")

                    try:
                        # First, receive the length of the incoming message (4 bytes, big-endian)
                        raw_msglen = self.__recv_all(conn, 4)
                        if not raw_msglen:
                            return
                        msglen = struct.unpack('>I', raw_msglen)[0]
                        
                        # Now, receive the actual message based on the length
                        received_data = self.__recv_all(conn, msglen)
                        if not received_data:
                            return

                        # Decode the received bytes into a string
                        message_str = received_data.decode()
                        # print(f"Received message: {message_str}")

                        # Deserialize the JSON string to a Python dictionary
                        message = json.loads(message_str)

                        # Handle the command and payload
                        command = message.get("command")
                        payload = message.get("payload")
                        
                        response_str = self.__command_handler(command, payload)
                        response_bytes = response_str.encode()
                        # Send the response length and the response itself
                        conn.sendall(struct.pack('>I', len(response_bytes)))
                        conn.sendall(response_bytes)

                    except json.JSONDecodeError:
                        print("Failed to decode JSON message")
                    
                    # print("Disconnecting from client.")
        print("Done.")
        
    def __recv_all(self, conn, length):
        """
        Receive all of the data from a socket, given a length.

        :param conn: The socket connection to receive from.
        :param length: The number of bytes to receive.
        :return: The received data as a bytes object, or None if a zero-length packet is received.
        """
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data
    
    def __command_handler(self, command, payload):
        """
        Handle commands and payloads from clients.

        Args:
            command (str): Command sent by the client.
            payload (dict): Payload sent by the client.

        Returns:
            str: JSON response containing the result of the command.
        """
                
        if command == "FMS": # Find my scooter
            prev_status = self.scooter_handler.get_status()
            self.sense_handler.display_status("Find Me")
            self.sense_handler.display_status(prev_status)
            return json.dumps({"message": "success"})
        
        elif command == "USS": # Update scooter status
            # print(f"Updating scooter status: ", payload.get("status"))
            self.scooter_handler.set_status(payload.get("status"))
            return json.dumps({"message": "success"})