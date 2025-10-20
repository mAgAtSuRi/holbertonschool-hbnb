import pytest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place


@pytest.fixture
def user():
    return User(first_name="John", last_name="Doe", email="john.doe@example.com", password="hello")


@pytest.fixture
def place(user):
    return Place(title="Nice place", description="Very nice",
                 price=100.0, latitude=45.0, longitude=10.0,
                 owner_id=user.id)


@pytest.fixture
def review(user, place):
    return Review(user_id=user.id, place_id=place.id, comment="Great stay!", rating=5)


def test_review_creation(review, user, place):
    assert review.user_id == user.id
    assert review.place_id == place.id
    assert review.comment == "Great stay!"
    assert 1 <= review.rating <= 5


def test_review_missing_comment(user, place):
    with pytest.raises(TypeError):
        Review(user_id=user.id, place_id=place.id, rating=4)


def test_review_invalid_rating(user, place):
    with pytest.raises(ValueError):
        Review(user_id=user.id, place_id=place.id, comment="Bad", rating=6)
