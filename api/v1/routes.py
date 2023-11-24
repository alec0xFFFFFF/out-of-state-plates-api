
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_access_token
from api.api import create_api
from api.services.factory import create_user_service, create_recommendation_service
from data.models import db
import psycopg2
from psycopg2 import pool
import boto3
import uuid
import openai

bp = Blueprint('bp', __name__)

user_service = create_user_service(db)
recommendation_service = create_recommendation_service(db)

def test_db_connection():
    try:
        # Attempting a simple query to test the connection
        result = db.engine.execute("SELECT 1")
        print("Database connection successful.")
        result.close()  # Close the result object to free resources
    except OperationalError:
        print("Database connection failed.")

# Run the function to test the connection
test_db_connection()

        
# TODO get restaurants
# TODO get user's meals
# TODO get recommendations


@bp.route('/', methods=['POST'])
def log_meal():
    user_id = get_jwt_identity()
    response = recommendation_service.add_meal(request.json, user_id)

    return jsonify(response)

# Login endpoint
@bp.route('/login', methods=['POST'])
def login():

    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        login_result = user_service.login(username, password)
        return jsonify(login_result), 200
    except InvalidCredentialsError as e:
        return jsonify({"error": e.message}), 401

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = user_service.register(data['username'], data['email'], data['phone-number'], data['password'], data['name'])

    # Create JWT token
    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token), 201

# Protected route
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@bp.route('/', methods=['GET'])
def hello_world():
    response = {"status": "success", "message": "hello world! welcome to out of state plates"}
    return jsonify(response), 200

def init_api_v1(app):
    app.register_blueprint(bp, url_prefix='/api/v1')
