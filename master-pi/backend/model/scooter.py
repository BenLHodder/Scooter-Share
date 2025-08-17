class Scooter:
    def __init__(self, scooterID, make, colour, longitude, latitude, costMin, batteryPercentage, status, ipAddress, faultNotes):
        self.scooterID = scooterID
        self.make = make
        self.colour = colour
        self.longitude = longitude
        self.latitude = latitude
        self.costMin = costMin
        self.batteryPercentage = batteryPercentage
        self.status = status
        self.ipAddress = ipAddress
        self.faultNotes = faultNotes

    def to_dict(self):
        """Convert the scooter object to a dictionary."""
        return {
            'scooterID': self.scooterID,
            'make': self.make,
            'colour': self.colour,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'costMin': self.costMin,
            'batteryPercentage': self.batteryPercentage,
            'status': self.status,
            'ipAddress': self.ipAddress,
            'faultNotes': self.faultNotes
        }

    @classmethod
    def from_dict(cls, data):
        """Create a scooter object from a dictionary."""
        return cls(
            scooterID=data['scooterID'],
            make=data['make'],
            colour=data['colour'],
            longitude=data['longitude'],
            latitude=data['latitude'],
            costMin=data['costMin'],
            batteryPercentage=data['batteryPercentage'],
            status=data['status'],
            ipAddress=data.get('ipAddress'),
            faultNotes=data.get('faultNotes')
        )

    def __str__(self):
        """Return a string representation of the scooter object."""
        return (f"Scooter(scooterID={self.scooterID}, make={self.make}, colour={self.colour}, "
                f"longitude={self.longitude}, latitude={self.latitude}, costMin={self.costMin}, "
                f"batteryPercentage={self.batteryPercentage}, status={self.status}, "
                f"ipAddress={self.ipAddress}, faultNotes={self.faultNotes})")
