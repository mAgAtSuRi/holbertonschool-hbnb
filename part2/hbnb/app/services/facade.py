from ..persistence.repository import InMemoryRepository
from ..models.user import User
from ..models.amenity import Amenity
from ..models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

# User methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()

    def update(self, user_id, data):
        return self.user_repo.update(user_id, data)

#   Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data), 200
    
    # Place methods
    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        if owner_id:
            if not self.user_repo.get(owner_id):
                raise LookupError(f"Owner id not found: {owner_id}")

        amenities_ids = place_data.pop("amenities", None)
        place = Place(**place_data)

        if amenities_ids:
            for amenity_id in amenities_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
                else:
                    raise LookupError(f"Amenity id not found: {amenity_id}")

        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        self.place_repo.update(place_id, place_data)
