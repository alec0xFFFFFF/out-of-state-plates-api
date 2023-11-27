from data.models import User

class InvalidCredentialsError(Exception):
    """Exception raised for invalid credentials."""

    def __init__(self, message="Invalid username or password"):
        self.message = message
        super().__init__(self.message)


class UserService:
  def __init__(self, db):
    self.db = db

  def login(self, username, phone, email, password):
      # todo by username, phone number or  email address
    
    user = User.query.filter_by(username=username).first()
    u2 = User.query.filter_by(email=email).first()
    u3 = User.query.filter_by(phone=phone).first()
    print(user)
    print(u2)
    print(u3)
    if user and check_password_hash(user.password_hash, password):
        return create_access_token(identity=username)
    raise InvalidCredentialsError()

  def register(self, username, email, phone, password, name):
      user = User(username=username, email=email, phone=phone, name=name)
      user.set_password(password)
      self.db.session.add(user)
      self.db.session.commit()
      return user
