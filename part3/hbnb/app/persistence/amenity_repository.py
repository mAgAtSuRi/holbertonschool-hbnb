from app.models.amenity import Amenity
from ..extensions import db
from .sqlalchemy_repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity) 

    def get_by_id(self, place_id):
        return Amenity.query.get(place_id)

    def update(self, amenity_id, data):
        amenity = self.get_by_id(amenity_id)
        if not amenity:
            raise LookupError(f"Amenity not found: {amenity_id}")

        for key, value in data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)

        db.session.commit()
        return amenity
