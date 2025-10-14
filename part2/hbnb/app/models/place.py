from base import Base


class Place(Base):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
    
    def update(self, data):
        """Update the attributes of the Place instance based on a dictionary"""
        allowed_changed = {"title", "description", "price",
                           "latitude", "longitude", "owner"}
        for key, value in data.items():
            if key in allowed_changed:
                setattr(self, key, value)
        self.save()