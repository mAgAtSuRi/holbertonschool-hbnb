from .baseclass import BaseModel
from ..extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import ForeignKey


class Review(BaseModel):
    __tablename__ = "reviews"

    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False) 

    @validates("rating")
    def validate_rating(self, key, value):
        if not 1 <= value <= 5 or not isinstance(value, int):
            raise ValueError("Rating must be a number between 1 and 5")
        return value

    @validates("comment")
    def validate_comment(self, key, value):
        if not value or not value.strip():
            raise ValueError("Comment can't be empty")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "comment": self.comment,
            "rating": self.rating      
        }
