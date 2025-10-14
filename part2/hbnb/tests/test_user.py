import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.user import User


def test_user_creation():
    user = User(first_name="John", last_name="Doe",
                email="john.doe@example.com", password="hello")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.check_password("hello")
    assert user.is_admin is False  # Default value
    print("User creation test passed!")


test_user_creation()
