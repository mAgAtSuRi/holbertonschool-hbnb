from ..models.user import User
from ..models.amenity import Amenity
from ..models.place import Place
from ..models.review import Review
from ..persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from werkzeug.security import generate_password_hash


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

# User methods
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update(self, user_id, data):
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])
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
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)

    # Review methods
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all()
                if review.place_id == place_id]   

    def update_review(self, review_id, review_data):
        review = self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review
