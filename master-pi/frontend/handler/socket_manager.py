import socket
import struct
import json
from pathlib import Path

class SocketManager:
    _instance = None

    def __new__(cls):
        base_dir = Path(__file__).resolve().parent.parent
        resource_file = base_dir / 'resources.json'
        
        if cls._instance is None:
            cls._instance = super(SocketManager, cls).__new__(cls)
            with open(resource_file, "r") as file:
                data = json.load(file)
                cls._instance.host = data["master-pi-IP"]
                cls._instance.port = data["master-pi-PORT"]
            cls._instance.address = (cls._instance.host, cls._instance.port)
        return cls._instance

    def send_and_receive(self, message):
        """Send data to the Master Pi and receive a response"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.address)
            message_bytes = json.dumps(message).encode()
            s.sendall(struct.pack(">I", len(message_bytes)))
            s.sendall(message_bytes)

            raw_msglen = self.recv_all(s, 4)
            if not raw_msglen:
                raise ConnectionError("No response from server.")

            msglen = struct.unpack(">I", raw_msglen)[0]
            response_data = self.recv_all(s, msglen)
            return json.loads(response_data.decode())

    def recv_all(self, sock, length):
        """Helper function to receive all bytes"""
        data = b""
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data
