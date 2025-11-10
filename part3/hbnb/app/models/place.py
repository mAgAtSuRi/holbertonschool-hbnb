from .baseclass import BaseModel
from ..extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import ForeignKey


amenities_places = db.Table(
    'amenities_places',
    db.Column('amenity_id', db.String(60), ForeignKey('amenities.id'), primary_key=True),
    db.Column('place_id', db.String(60), ForeignKey('places.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    reviews = db.relationship("Review", backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=amenities_places, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    @validates("title")
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Title can't be empty")
        return value.strip()

    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative float")
        return float(value)

    @validates("latitude")
    def validate_latitude(self, key, value):
        if value is not None and not -90 <= value <= 90:
            raise ValueError("Latitude shoud be between -90 and 90")
        return value

    @validates("longitude")
    def validate_longitude(self, key, value):
        if value is not None and not -180 <= value <= 180:
            raise ValueError("Longitude shoud be between -180 and 180")
        return value

    def add_amenity(self, amenity):
        """Add an amenity to the place if not already added"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def update(self, data):
        """Prevent changing owner"""
        if "owner" in data:
            raise ValueError("Can't change the owner of a place.")
        super().update(data)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [
                {"id": a.id, "name": a.name, "description": getattr(a, "description", None)}
                for a in self.amenities
            ] if self.amenities else []
        }
