from typing import List, Optional

from sqlalchemy import select
from models.enums import TasksStatusEnum
from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from models.entity import UsersModel, TasksModel

class TasksRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task_by_id(self, task_id: int):
        result = await self.session.execute(select(TasksModel).where(TasksModel.id == task_id))
        return result.scalar_one_or_none()

    async def get_tasks_for_customer(self, user_id: int):
        result = await self.session.execute(select(TasksModel).where(TasksModel.user_id == user_id))
        return result.scalars()

    async def get_history_tasks(self, user_id: int):
        result = await self.session.execute(
            select(TasksModel).where(
                TasksModel.user_id == user_id,
                TasksModel.status.notin_([TasksStatusEnum.CREATED, TasksStatusEnum.PROCESSING])
            )
        )
        return result.scalars()

    async def get_open_tasks(self, user_id: int):
        result = await self.session.execute(
            select(TasksModel).where(
                TasksModel.user_id == user_id,
                TasksModel.status.notin_([TasksStatusEnum.CANCELLED, TasksStatusEnum.COMPLETED])
            )
        )
        return result.scalars()

    async def get_user(self, auth_id: int):
        result = await self.session.execute(select(UsersModel).where(UsersModel.auth_id == auth_id))
        return result.scalar_one_or_none()


    async def create_task(self, model: TasksModel):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_task_by_id(self, task_id: int):
        result = await self.session.execute(select(TasksModel).where(TasksModel.id == task_id))
        return result.scalar_one_or_none()

    async def update_task(self, model: TasksModel):
        await self.session.commit()
        await self.session.refresh(model)
        return model

def get_tasks_repository(session: AsyncSession = Depends(get_session)) -> TasksRepository:
    return TasksRepository(session)
