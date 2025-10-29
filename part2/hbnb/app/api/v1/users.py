from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ...services import facade

api = Namespace("users", description="User operations")

# Define the user model for input validation and documentation
user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True, description="First name of the user"
        ),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)


@api.route("/")
class UserList(Resource):
    @api.doc(security='Bearer')
    @api.response(403, "Access forbidden")
    @jwt_required()
    def get(self):
        # Only admin can get the user list
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {"error": "Admin access required"}, 403
        return [element.to_dict() for element in facade.get_all_users()]

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<user_id>")
class UserResource(Resource):
    @api.doc(security='Bearer')
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        if current_user_id != user_id and not claims.get("is_admin", False):
            return {"error": "Access forbidden"}, 403

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 200

    @api.doc(security='Bearer')
    @api.response(200, "User details retrieved successfully")
    @api.response(400, "Bad request")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if current_user != user_id and not claims.get("is_admin", False):
            return {"error": "Access forbidden"}, 403

        new_user_data = api.payload
        user = facade.get_user(user_id)

#       Check if user exists
        if not user:
            return {"error": "User not found"}, 404
#       Check if email is not already used
        existing_user = facade.get_user_by_email(new_user_data["email"])
        if existing_user and user_id != existing_user.id:
            return {"error": "Email already registered"}, 400

        facade.update(user_id, new_user_data)
        updated_user = facade.get_user(user_id)

        return {
            "id": updated_user.id,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "email": updated_user.email
        }, 200
