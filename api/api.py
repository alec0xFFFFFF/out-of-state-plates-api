from flask import Flask
from flask_jwt_extended import JWTManager
from data.models import db
import os

def create_api():
    app = Flask(__name__)

    # Authentication configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("PG_DB_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)    
    jwt = JWTManager(app)

    # Import routes after db to avoid circular imports
    from api.v1.routes import init_api_v1
    init_api_v1(app)

    return app

