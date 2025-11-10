from .baseclass import BaseModel
from ..extensions import db


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
