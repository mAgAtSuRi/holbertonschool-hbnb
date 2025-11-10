import pytest
from app.models.amenity import Amenity


@pytest.fixture
def amenity():
    return Amenity(name="Pool", description="A nice swimming pool")


def test_amenity_creation(amenity):
    assert amenity.name == "Pool"
    assert amenity.description == "A nice swimming pool"


def test_amenity_missing_name():
    with pytest.raises(TypeError):
        Amenity(description="Missing name")
