from flask import Flask
from flask_jwt_extended import JWTManager
from data.models import db
import os

db_params = {
    "dbname": os.environ.get("PGDATABASE"),
    "user": os.environ.get("PGUSER"),
    "password": os.environ.get("PGPASSWORD"),
    "host": os.environ.get("PGHOST"),
    "port": int(os.environ.get("PGPORT"))
}

def create_api():
    app = Flask(__name__)

    # Authentication configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
    # Configure JWT to expire in a different duration
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(months=1)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)    
    jwt = JWTManager(app)

    # Import routes after db to avoid circular imports
    from api.v1.routes import init_api_v1
    init_api_v1(app)

    return app

