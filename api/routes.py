import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from api.api import create_api
import psycopg2
from psycopg2 import pool
import boto3
import uuid
import openai

bp = Blueprint('bp', __name__)

class PostgresPool:
    def __init__(self, minconn, maxconn, **db_params):
        self._pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, **db_params)

    def get_connection(self):
        try:
            return self._pool.getconn()
        except Exception as e:
            print(f"Error acquiring connection: {e}")
            return None

    def release_connection(self, connection):
        try:
            self._pool.putconn(connection)
        except Exception as e:
            print(f"Error releasing connection: {e}")

    def close_all_connections(self):
        try:
            self._pool.closeall()
        except Exception as e:
            print(f"Error closing connections: {e}")

# Database and AWS S3 configuration
db_params = {
    "dbname": os.environ.get("PGDATABASE"),
    "user": os.environ.get("PGUSER"),
    "password": os.environ.get("PGPASSWORD"),
    "host": os.environ.get("PGHOST"),
    "port": int(os.environ.get("PGPORT"))
}
print("connected to database: " + db_params["dbname"]  + " on "  + db_params["host"] + ":" + str(db_params["port"]) + " as user: " + db_params["user"])
db_pool = PostgresPool(minconn=1, maxconn=10, **db_params)

s3_client = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_KEY_ID"))

# OpenAI API configuration
openai.api_key = os.environ.get("OPENAI_KEY_NAME")

def upload_image_to_s3(file):
    try:
        file_key = str(uuid.uuid4())  # Generate unique file name
        s3_client.upload_fileobj(file, os.environ.get("IMAGE_BUCKET_NAME"), file_key)
        return f"https://{YOUR_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

def get_openai_embedding(text):
    try:
        response = openai.Embedding.create(input=text, model="text-similarity-babbage-001")
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
        
# TODO get restaurants
# TODO get user's meals
# TODO get recommendations


@bp.route('/', methods=['POST'])
def log_meal():
    price = request.form.get('price')
    restaurant_name = request.form.get('restaurant_name')
    cuisine = request.form.get('cuisine')
    description = request.form.get('description')
    image_urls = []

    if 'images' in request.files:
        for image in request.files.getlist('images'):
            image_url = upload_image_to_s3(image)
            if image_url:
                image_urls.append(image_url)

    # Generate embeddings for the description
    embedding = get_openai_embedding(description)
    if embedding is None:
        return jsonify({"status": "error", "message": "Failed to generate embedding"})

    conn = db_pool.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO meal (price, restaurant_name, cuisine, description, images, embedding) VALUES (%s, %s, %s, %s, %s, cube(array[%s]))"
            cursor.execute(query, (price, restaurant_name, cuisine, description, image_urls, ','.join(map(str, embedding))))
            conn.commit()
            response = {"status": "success"}
        except Exception as e:
            conn.rollback()
            response = {"status": "error", "message": str(e)}
        finally:
            db_pool.release_connection(conn)
    else:
        response = {"status": "error", "message": "Unable to connect to the database"}

    return jsonify(response)

# Login endpoint
@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401

# Protected route
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def init_app(app):
    app.register_blueprint(bp)
