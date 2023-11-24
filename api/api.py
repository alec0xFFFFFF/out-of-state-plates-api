from flask import Flask
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
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)    
    jwt = JWTManager(app)

    from api.routes import init_app
    init_app(app)

    return app

