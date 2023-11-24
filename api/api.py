from flask import Flask
from data.models import db

def create_api():
    app = Flask(__name__)

    # Authentication configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)    
    jwt = JWTManager(app)

    from api.routes import init_app
    init_app(app)

    return app

