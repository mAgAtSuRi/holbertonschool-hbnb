from .base import Base


class Review(Base):
    def __init__(self, place, user, rating, comment):
        super().__init__()
        self.place = place
        self.user = user
        self.rating = rating
        self.comment = comment

    def update(self, data):
        """Update the attributes of the Review instance
        based on a dictionary"""
        allowed_changed = {"rating", "comment"}
        for key, value in data.items():
            if key in allowed_changed:
                setattr(self, key, value)
        self.save()