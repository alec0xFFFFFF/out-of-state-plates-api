from data.models import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash


class InvalidCredentialsError(Exception):
    """Exception raised for invalid credentials."""

    def __init__(self, message="Invalid username or password"):
        self.message = message
        super().__init__(self.message)


class UserService:
  def __init__(self, db):
    self.db = db

  def login(self, username, email, phone, password):
    user = User.query.filter_by(username=username).first()
    if not user and email:
        user = User.query.filter_by(email=email).first()
    if not user and phone:
        user = User.query.filter_by(phone=phone).first()
    if user and check_password_hash(user.password_hash, password):
        print(f"user: {user.id} logged in")
        return create_access_token(identity=user.id)
    raise InvalidCredentialsError()

  def register(self, username, email, phone, password, name):
      user = User(username=username, email=email, phone=phone, name=name)
      user.set_password(password)
      self.db.session.add(user)
      self.db.session.commit()
      return user
