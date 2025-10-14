from base import Base


class Amenity(Base):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def update(self, data):
        """Update the attributes of the Amenity instance
        based on a dictionary"""
        allowed_changed = {"name", "description"}
        for key, value in data.items():
            if key in allowed_changed:
                setattr(self, key, value)
        self.save()