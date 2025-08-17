import socket


def get_local_ip():
    """Get the local IP address of the machine"""

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to an external server
        ip = s.getsockname()[0]
    except Exception as e:
        print(f"Error retrieving IP: {e}")
        ip = "127.0.0.1"  # Fallback to localhost
    finally:
        s.close()
    return ip
