from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

class TasksRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


def get_tasks_repository(session: AsyncSession = Depends(get_session)) -> TasksRepository:
    return TasksRepository(session)
