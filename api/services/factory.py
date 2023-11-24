from api.services.user_service import UserService
from api.services.recommendation_service import RecommendationService

def create_user_service(db):
    return UserService(db)
  
def create_recommendation_service(db):
    return RecommendationService(db)
