from app.models.place import Place
from ..extensions import db


class PlaceRepository:
    def create(self, data):
        place = Place(**data)
        db.session.add(place)
        db.session.commit()
        return place

    def get_all(self):
        return Place.query.all()

    def get_by_id(self, place_id):
        return Place.query.get(place_id)

    def update(self, place_id, data):
        place = self.get_by_id(place_id)
        if not place:
            raise LookupError(f"Place not found: {place_id}")

        # Error if owner try to change owner_id of the place
        if data.get("owner_id") != place.owner_id:
            raise ValueError("Can't change the owner of a place.")

        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        db.session.commit()
        return place
