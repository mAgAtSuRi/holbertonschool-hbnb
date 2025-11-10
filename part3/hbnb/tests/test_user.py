import pytest
from app.models.user import User


@pytest.fixture
def user():
    return User(first_name="John", last_name="Doe", email="john.doe@example.com", password="hello")


def test_user_creation(user):
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.check_password("hello")
    assert user.is_admin is False


def test_user_invalid_email():
    with pytest.raises(ValueError):
        User(first_name="Jane", last_name="Doe", email="invalid-email", password="hello")
