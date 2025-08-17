class FaultLog:
    def __init__(self, faultID, scooterID, startDateTime, status='Open', faultNotes=None, resolution=None, endDateTime=None):
        self.faultID = faultID
        self.scooterID = scooterID
        self.startDateTime = startDateTime
        self.status = status
        self.faultNotes = faultNotes
        self.resolution = resolution
        self.endDateTime = endDateTime

    def to_dict(self):
        """Convert the fault log object to a dictionary."""
        return {
            'faultID': self.faultID,
            'scooterID': self.scooterID,
            'startDateTime': self.startDateTime.isoformat() if self.startDateTime else None,
            'status': self.status,
            'faultNotes': self.faultNotes,
            'resolution': self.resolution,
            'endDateTime': self.endDateTime.isoformat() if self.endDateTime else None
        }

    @classmethod
    def from_dict(cls, data):
        """Create a fault log object from a dictionary."""
        return cls(
            faultID=data['faultID'],
            scooterID=data['scooterID'],
            startDateTime=data['startDateTime'],
            status=data['status'],
            faultNotes=data['faultNotes'],
            resolution=data.get('resolution'),
            endDateTime=data.get('endDateTime')
        )
        
    def __str__(self):
        """Return a string representation of the fault log object."""
        return (f"FaultLog(faultID={self.faultID}, scooterID={self.scooterID}, "
                f"startDateTime={self.startDateTime}, status={self.status}, "
                f"faultNotes={self.faultNotes}, resolution={self.resolution}, "
                f"endDateTime={self.endDateTime})")
