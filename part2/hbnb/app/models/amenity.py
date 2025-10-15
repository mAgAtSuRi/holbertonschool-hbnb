from .base import Base


class Amenity(Base):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }