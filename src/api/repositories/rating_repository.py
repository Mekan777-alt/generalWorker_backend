from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from database.session import get_session

class RatingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


def get_rating_repository(session: AsyncSession = Depends(get_session)) -> RatingRepository:
    return RatingRepository(session)
