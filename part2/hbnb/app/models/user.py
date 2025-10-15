from .base import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = generate_password_hash(password)
        self.is_admin = is_admin

    @property
    def password(self):
        raise AttributeError("Acces to password is forbidden")
    
    @password.setter
    def password(self, value):
        self.__password = generate_password_hash(value)
    
    def check_password(self, password):
        return check_password_hash(self.__password, password)

    def update(self, data):
        """Update the attributes of the User instance,
        including password hashing if needed"""

        if "password" in data:
            self.__password = generate_password_hash(data["password"])
#       call update without password
        super().update({k: v for k, v in data.items() if k != "password"})

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
