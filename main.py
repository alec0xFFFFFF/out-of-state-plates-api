from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import pool
import boto3
import uuid
import openai

# Assuming PostgresPool class is already defined

app = Flask(__name__)

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
    "dbname": "your_dbname",
    "user": "your_username",
    "password": "your_password",
    "host": "your_host",
    "port": "your_port"
}
db_pool = PostgresPool(minconn=1, maxconn=10, **db_params)

s3_client = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

# OpenAI API configuration
openai.api_key = 'YOUR_OPENAI_API_KEY'

def upload_image_to_s3(file):
    try:
        file_key = str(uuid.uuid4())  # Generate unique file name
        s3_client.upload_fileobj(file, 'YOUR_BUCKET_NAME', file_key)
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

@app.route('/write', methods=['POST'])
def write_to_db():
    # ... (Same as before for handling price, restaurant_name, cuisine, description, images)

    # Generate embeddings for the description
    embedding = get_openai_embedding(description)
    if embedding is None:
        return jsonify({"status": "error", "message": "Failed to generate embedding"})

    conn = db_pool.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO your_table (price, restaurant_name, cuisine, description, images, embedding) VALUES (%s, %s, %s, %s, %s, cube(array[%s]))"
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

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

