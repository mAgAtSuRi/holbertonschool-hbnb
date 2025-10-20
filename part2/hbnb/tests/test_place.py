import pytest
from app.models.place import Place
from app.models.user import User


@pytest.fixture
def user():
    return User(first_name="John", last_name="Doe", email="john.doe@example.com", password="hello")


@pytest.fixture
def place(user):
    return Place(title="Nice place", description="Very nice",
                 price=100.0, latitude=45.0, longitude=10.0,
                 owner_id=user.id)


def test_place_creation(place, user):
    assert place.title == "Nice place"
    assert place.owner_id == user.id
    assert place.price == 100.0
    assert -90 <= place.latitude <= 90
    assert -180 <= place.longitude <= 180


def test_place_missing_title(user):
    with pytest.raises(TypeError):
        Place(description="No title", price=50.0, latitude=0, longitude=0, owner_id=user.id)
