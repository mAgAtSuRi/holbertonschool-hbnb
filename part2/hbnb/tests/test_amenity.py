from app.models.amenity import Amenity


def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi", description="High debit connection")
    assert amenity.name == "Wi-Fi"
    assert amenity.description == "High debit connection"


test_amenity_creation()