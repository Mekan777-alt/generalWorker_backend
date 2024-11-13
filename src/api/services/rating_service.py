from fastapi import Depends

from api.repositories.auth_repository import AuthRepository, get_auth_repository
from api.repositories.rating_repository import get_rating_repository, RatingRepository

class RatingService:
    def __init__(self, rating_repository: RatingRepository, auth_repository: AuthRepository):
        self.rating_repository = rating_repository
        self.auth_repository = auth_repository


    async def get_rating_current_user(self, current_user: dict):
        pass


def get_rating_service(rating_repository: RatingRepository = Depends(get_rating_repository),
                       auth_repository: AuthRepository = Depends(get_auth_repository)) -> RatingService:
    return RatingService(rating_repository=rating_repository, auth_repository=auth_repository)
