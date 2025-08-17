class Transaction:
    def __init__(self, transactionID, email, transactionAmount, datetime):
        self.transactionID = transactionID
        self.email = email
        self.transactionAmount = transactionAmount
        self.datetime = datetime

    def to_dict(self):
        """Convert the transaction object to a dictionary."""
        return {
            'transactionID': self.transactionID,
            'email': self.email,
            'transactionAmount': self.transactionAmount,
            'datetime': self.datetime
        }

    @classmethod
    def from_dict(cls, data):
        """Create a transaction object from a dictionary."""
        return cls(
            transactionID=data['transactionID'],
            email=data['email'],
            transactionAmount=data['transactionAmount'],
            datetime=data['datetime']
        )

    def __str__(self):
        """Return a string representation of the transaction object."""
        return (f"Transaction(transactionID={self.transactionID}, email={self.email}, "
                f"transactionAmount={self.transactionAmount}, datetime={self.datetime})")
