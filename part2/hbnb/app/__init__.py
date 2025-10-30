from flask import Flask
from flask_restx import Api
from config import config
from .extensions import db, jwt

from .api.v1.users import api as users_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns
from .api.v1.auth import api as auth_ns
from .services import facade


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # Initialize extensions
    jwt.init_app(app)
    db.init_app(app)

    # Register namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Create admin within application context
    # with app.app_context():
    #     if not facade.get_user_by_email("admin@example.com"):
    #         facade.create_user({
    #             "first_name": "Admin",
    #             "last_name": "Admin",
    #             "email": "admin@example.com",
    #             "password": "admin123",
    #             "is_admin": True
    #         })

    return app
