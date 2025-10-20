from .base import Base


class Review(Base):
    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not 1 <= value <= 5 or not isinstance(value, int):
            raise ValueError("Rating must be a number between 1 and 5")
        self._rating = value

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "comment": self.comment,
            "rating": self.rating         
        }
