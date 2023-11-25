import boto3
import os
from openai import OpenAI
import uuid
from data.models import Meal, Restaurant
from enum import Enum

class Classification(Enum):
   RECIPE = 1
   RESTAURANT = 2
   EITHER = 3
   
class RecommendationService:
  # todo log ingredients
  # for cooking inject ingredients

  # todo for restaurants inject new that other users enjoyed based on user's preferences
  # todo inject based on location
  # todo inject based on what's retrieved from embeddings

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
  
  def _classify(self, msg):
     completion = self.openai_client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "Classify the user's message to recommend either a recipe, a restaurant or either. Return just recipe if the user is looking for a recipe. Return just restaurant if the user is looking for a restaurant recommendation."},
        {"role": "user", "content": request.get('message')}
      ]
      )
     resp = completion.choices[0].message
     print(resp.content)
     if resp.content == "recipe":
        return Classification.RECIPE
     elif resp.content == "restaurant":
        return Classification.RESTAURANT
     return Classification.EITHER

  def get_recommendation(self, request, user_id):
    print(request)
    classification = self._classify(request.get('message'))
    completion = self.openai_client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are Sous a helpful dining and cooking assistant. Your goal is to help a user pick what to eat being as specific as possible. Give recommendations based on the user's inquiry. For what to cook format the recipe and ingredients so it's easy to purchase and follow. For restaurants give multiple options and describe what to order. Limit the response to around 30 tokens and only either recommends restaurants or a recipe but not both."},
        {"role": "user", "content": request.get('message')}
      ]
    )

    resp = completion.choices[0].message
    print(resp.content)
    return {"message": resp.content}
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
