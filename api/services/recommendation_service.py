import boto3
import os
from openai import OpenAI
import uuid
from data.models import Meal, Restaurant

class RecommendationService:
  def __init__(self, db):
    self.db = db
    self.s3_client = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_KEY_ID"))
    # OpenAI API configuration
    self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_KEY_NAME"))

  def add_restaurant(self, restaurant):
    raise NotImplementedError("add_restaurant must be implemented")

  def add_meal(self, request, user_id):
    price = request.form.get('price')
    restaurant_name = request.form.get('restaurant_name')
    cuisine = request.form.get('cuisine')
    description = request.form.get('description')
    image_urls = []

    if 'images' in request.files:
        for image in request.files.getlist('images'):
            image_url = self._upload_image_to_s3(image)
            if image_url:
                image_urls.append(image_url)

    # Generate embeddings for the description
    embedding = self._get_openai_embedding(description)
    if embedding is None:
        raise Exception("Unable to generate embeddings")

    # todo user_id, restaurant_id
    meal = Meal(
        user_id, price, restaurant_name, cuisine, description, image_urls, embedding
    )
    db.session.add(meal)
    db.session.commit()
    return {"status": "success"}

  def get_recommendation(self, request, user_id):
    completion = self.openai_client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": request.form.get('message')}
      ]
    )

    resp = completion.choices[0].message
    return {"message": resp}
    raise NotImplementedError("get_recommendation must be implemented")

  def _upload_image_to_s3(file):
    try:
        file_key = str(uuid.uuid4())  # Generate unique file name
        s3_client.upload_fileobj(file, os.environ.get("IMAGE_BUCKET_NAME"), file_key)
        return f'https://{os.environ.get("IMAGE_BUCKET_NAME")}.s3.amazonaws.com/{file_key}'
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
