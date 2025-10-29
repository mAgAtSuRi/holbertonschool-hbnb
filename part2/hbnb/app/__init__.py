from flask import Flask
from flask_restx import Api
from .api.v1.users import api as users_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns
from .api.v1.auth import api as auth_ns
from config import config
from flask_jwt_extended import JWTManager
from .services import facade

jwt = JWTManager()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # Create admin if it doesn't exist already
    if not facade.get_user_by_email("admin@example.com"):
        facade.create_user({
            "first_name": "Admin",
            "last_name": "Admin",
            "email": "admin@example.com",
            "password": "admin123",
            "is_admin": True
        })
    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # Login
    api.add_namespace(auth_ns, path='/api/v1/auth')

    jwt.init_app(app)
    return app
