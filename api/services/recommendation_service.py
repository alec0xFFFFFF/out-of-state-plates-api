import boto3
import os
import openai
import uuid

class RecommendationService:
  def __init__(self, db):
    self.db = db
    self.s3_client = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_KEY_ID"))
    # OpenAI API configuration
    self.openai.api_key = os.environ.get("OPENAI_KEY_NAME")

  def add_restaurant(self, restaurant):
    raise NotImplementedError("add_restaurant must be implemented")

  def add_meal(self, meal):
    raise NotImplementedError("add_meal must be implemented")

  def get_recommendation(self, request):
    raise NotImplementedError("get_recommendation must be implemented")

  def _upload_image_to_s3(file):
    try:
        file_key = str(uuid.uuid4())  # Generate unique file name
        s3_client.upload_fileobj(file, os.environ.get("IMAGE_BUCKET_NAME"), file_key)
        return f"https://{os.environ.get("IMAGE_BUCKET_NAME")}.s3.amazonaws.com/{file_key}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

def _get_openai_embedding(text):
    try:
        response = openai.Embedding.create(input=text, model="text-similarity-babbage-001")
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
