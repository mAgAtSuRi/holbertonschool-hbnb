from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ...services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    "description": fields.String(
            required=True, description="Description of the amenity"
        )
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner'),
    'password': fields.String(required=True, description='Password of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):

    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        place_data = api.payload
        current_user = get_jwt_identity()
        claims = get_jwt()
        if current_user != place_data.get('owner_id') and not claims.get("is_admin", False):
            return {"error": "Access forbidden"}, 403

        required_field = ["title", "description", "price", "latitude",
                          "longitude", "owner_id"]
        for field in required_field:
            if not place_data.get(field):
                return {"error": f"Missing required field: {field}"}, 400

        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            return {"error": f"Owner id not found: {place_data['owner_id']}"}, 404

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        places = facade.get_all_places()
        return [{
            "id": place.id,
            "title": place.title,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "amenities": [
                {"id": a.id, "name": a.name}
                for a in place.amenities
                ] if place.amenities else []
            }
            for place in places
        ]


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)
        if not owner:
            return {"error": "Owner not found"}, 404

        data = place.to_dict()
        data["owner"] = {
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        }

        data.pop("owner_id", None)
        return data, 200

    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        new_place_data = api.payload
        current_user = get_jwt_identity()
        claims = get_jwt() 
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if current_user != place.owner_id and not claims.get("is_admin", False):
            return {"error": "Access forbidden"}, 403

        required_field = ["title", "description", "price", "latitude",
                          "longitude", "owner_id"]
        for field in required_field:
            if field not in new_place_data:
                return {"error": f"Missing required field: {field}"}, 400

        try:
            facade.update_place(place_id, new_place_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        facade.update_place(place_id, new_place_data)
        updated_place = facade.get_place(place_id)

        return updated_place.to_dict()


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
