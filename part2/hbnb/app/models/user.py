from .base import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update(self, data):
        """Update the attributes of the User instance,
        including password hashing if needed"""

        allowed_changed = {"first_name", "last_name", "email", "password"}
        for key, value in data.items():
            if key in allowed_changed:
                if key == "password":
                    value = generate_password_hash(value)
                setattr(self, key, value)
        self.save()