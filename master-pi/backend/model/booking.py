class Booking:
    def __init__(self, bookingID, email, scooterID, startDateTime, endDateTime=None, actualStartDateTime=None, actualEndDateTime=None, cost=None, depositCost=None, status='Active', googleID=None):
        self.bookingID = bookingID
        self.email = email
        self.scooterID = scooterID
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime
        self.actualStartDateTime = actualStartDateTime
        self.actualEndDateTime = actualEndDateTime
        self.cost = cost
        self.depositCost = depositCost
        self.status = status
        self.googleID = googleID  # New attribute

    def to_dict(self):
        """Convert the booking object to a dictionary."""
        return {
            'bookingID': self.bookingID,
            'email': self.email,
            'scooterID': self.scooterID,
            'startDateTime': self.startDateTime,
            'endDateTime': self.endDateTime,
            'actualStartDateTime': self.actualStartDateTime,
            'actualEndDateTime': self.actualEndDateTime,
            'cost': self.cost,
            'depositCost': self.depositCost,
            'status': self.status,
            'googleID': self.googleID  # Include googleID in the dictionary
        }

    @classmethod
    def from_dict(cls, data):
        """Create a booking object from a dictionary."""
        return cls(
            bookingID=data.get('bookingID'),
            email=data.get('email'),
            scooterID=data.get('scooterID'),
            startDateTime=data.get('startDateTime'),
            endDateTime=data.get('endDateTime'),
            actualStartDateTime=data.get('actualStartDateTime'),
            actualEndDateTime=data.get('actualEndDateTime'),
            cost=data.get('cost'),
            depositCost=data.get('depositCost'),
            status=data.get('status', 'Active'),  # Default to 'Active' if status is not provided
            googleID=data.get('googleID')  # Retrieve googleID from the data
        )

    def __str__(self):
        """Return a string representation of the booking object."""
        return (f"Booking(bookingID={self.bookingID}, email={self.email}, scooterID={self.scooterID}, "
                f"startDateTime={self.startDateTime}, endDateTime={self.endDateTime}, "
                f"actualStartDateTime={self.actualStartDateTime}, actualEndDateTime={self.actualEndDateTime}, "
                f"cost={self.cost}, depositCost={self.depositCost}, status={self.status}, googleID={self.googleID})")
