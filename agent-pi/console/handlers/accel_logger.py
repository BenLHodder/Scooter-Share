import threading
import time
import csv
from handlers.sense_handler import sense_handler

class AccelLogger:
    def __init__(self, sense, file_path):
        self.sense = sense
        self.file_path = file_path
        self.timer = None
        self.running = False
        
    def write_header(self):
        """Write the header to the file."""
        with open(self.file_path, 'w') as f:
            f.write("x, y, z\n")

    def save_accel_to_file(self, interval):
        """Save accelerometer data to a file."""
        with open(self.file_path, 'a') as f:
            while self.running:
                acceleration = self.sense.get_acceleration()
                f.write(f"{acceleration['x']}, {acceleration['y']}, {acceleration['z']}\n")
                time.sleep(interval / 1000.0)

    def start_timer(self, interval):
        """Start the timer to save accelerometer data at specified intervals."""
        self.write_header()
        self.running = True
        self.timer = threading.Thread(target=self.save_accel_to_file, args=(interval,))
        self.timer.start()

    def stop_timer(self):
        """Stop the timer."""
        self.running = False
        if self.timer is not None:
            self.timer.join()  # Wait for the thread to finish
            
    def find_largest_acceleration(self, csv_file):
        """Find the largest acceleration value from the CSV file."""
        max_x = max_y = max_z = float('-inf')  # Initialize max values to negative infinity

        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)  # Read the CSV with headers
            for row in reader:
                try:
                    # Strip leading/trailing whitespace from keys and values
                    row = {key.strip(): value.strip() for key, value in row.items()}

                    # Ensure the values are not None before converting to float
                    x = float(row.get('x', float('-inf')))
                    y = float(row.get('y', float('-inf')))
                    z = float(row.get('z', float('-inf')))

                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
                    max_z = max(max_z, z)
                except (ValueError, TypeError) as e:
                    print(f"Error reading values: {e}")  # Handle potential conversion errors
        return max_x, max_y, max_z  # Return the largest values for each axis


# Example usage
# sense = sense_handler()
# logger = AccelLogger(sense, 'acceleration_data.csv')

# Start logging accelerometer data every X milliseconds (e.g., every 100 milliseconds)
# logger.start_timer(100)

# time.sleep(25)

# Call this when you want to stop logging
# logger.stop_timer()
