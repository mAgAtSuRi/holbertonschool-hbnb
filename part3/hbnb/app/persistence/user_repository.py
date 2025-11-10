from app.models.user import User
from ..extensions import db
from .sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User) 

    def get_user_by_email(self, email):
        """Return the user corresponding to the email, or None"""
        return self.model.query.filter_by(email=email).first()
