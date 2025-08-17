class User:
    def __init__(self, email, password, first_name, last_name, phone_no, funds, role):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_no = phone_no
        self.funds = funds
        self.role = role

    def to_dict(self):
        """Convert the user object to a dictionary."""
        return {
            'email': self.email,
            'password': self.password,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'phoneNo': self.phone_no,
            'funds': self.funds,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, data):
        """Create a user object from a dictionary."""
        return cls(
            email=data['email'],
            password=data['password'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            phone_no=data['phoneNo'],
            funds=data['funds'],
            role=data['role']
        )
        
    def __str__(self):
        """Return a string representation of the user object."""
        return f"User(email={self.email}, first_name={self.first_name}, last_name={self.last_name}, phone_no={self.phone_no}, funds={self.funds}, role={self.role})"


class Admin(User):
    def __init__(self, email, password, first_name, last_name, phone_no, funds):
        super().__init__(email, password, first_name, last_name, phone_no, funds, role='Admin')

    def __str__(self):
        """Return a string representation of the admin object."""
        return f"Admin(email={self.email}, first_name={self.first_name}, last_name={self.last_name}, phone_no={self.phone_no}, funds={self.funds})"


class Customer(User):
    def __init__(self, email, password, first_name, last_name, phone_no, funds):
        super().__init__(email, password, first_name, last_name, phone_no, funds, role='Customer')

    def __str__(self):
        """Return a string representation of the customer object."""
        return f"Customer(email={self.email}, first_name={self.first_name}, last_name={self.last_name}, phone_no={self.phone_no}, funds={self.funds})"


class Engineer(User):
    def __init__(self, email, password, first_name, last_name, phone_no, funds):
        super().__init__(email, password, first_name, last_name, phone_no, funds, role='Engineer')

    def __str__(self):
        """Return a string representation of the engineer object."""
        return f"Engineer(email={self.email}, first_name={self.first_name}, last_name={self.last_name}, phone_no={self.phone_no}, funds={self.funds})"
