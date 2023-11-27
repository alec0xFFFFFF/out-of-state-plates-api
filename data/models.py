from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, ForeignKey, DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, onupdate=datetime.utcnow)
    deleted = db.Column(Boolean, nullable=False, default=False)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'phone': self.phone,
            'created_at': self.created_at,
            'deleted': self.deleted
        }
  
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, onupdate=datetime.utcnow)
    deleted = db.Column(Boolean, nullable=False, default=False)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cuisine': self.cuisine,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted': self.deleted
        }

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.id'), nullable=True)
    homecooked = db.Column(Boolean, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_urls = db.Column(db.Text, nullable=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, onupdate=datetime.utcnow)
    deleted = db.Column(Boolean, nullable=False, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'restaurant_id': self.restaurant_id,
            'homecooked': self.homecooked,
            'cuisine': self.cuisine,
            'description': self.description,
            'price': self.price,
            'image_urls': self.image_urls,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted': self.deleted
        }

