class RecommendationService:
  def __init__(self, db):
    self.db = db

  def add_restaurant(self, restaurant):
    raise NotImplementedError("add_restaurant must be implemented")

  def add_meal(self, meal):
    raise NotImplementedError("add_meal must be implemented")

  def get_recommendation(self, request):
    raise NotImplementedError("get_recommendation must be implemented")
