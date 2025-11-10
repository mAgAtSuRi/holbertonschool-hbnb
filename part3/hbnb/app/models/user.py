from .baseclass import BaseModel
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates, relationship
import re


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship("Place", backref='owner', lazy=True)
    reviews = db.relationship("Review", backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @validates('email')
    def validate_email(self, key, value):
        if not value or not value.strip():
            raise ValueError("Email can't be empty")
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format")
        return value.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
