from .base import Base


class Review(Base):
    def __init__(self, place, user, rating, comment):
        super().__init__()
        self.place = place
        self.user = user
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        return {
            "comment": self.comment,
            "rating": self.rating,
            "user_id": user.
        }