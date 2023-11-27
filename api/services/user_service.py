from data.models import User

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
    print(user)
    if not user and email:
        user = User.query.filter_by(email=email).first()
        print(user)
    if not user and phone:
        user = User.query.filter_by(phone=phone).first()
        print(user)
    if user and check_password_hash(user.password_hash, password):
        return create_access_token(identity=username)
    raise InvalidCredentialsError()

  def register(self, username, email, phone, password, name):
      user = User(username=username, email=email, phone=phone, name=name)
      user.set_password(password)
      self.db.session.add(user)
      self.db.session.commit()
      return user
