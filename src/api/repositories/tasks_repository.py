from sqlalchemy import select
from models.enums import TasksStatusEnum
from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from models.entity import TasksModel, RoleModel, CustomerProfileModel, ExecutorProfileModel, TaskResponseModel


class TasksRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_customer_profile(self, auth_id: int):
        result = await self.session.execute(
            select(CustomerProfileModel).where(CustomerProfileModel.auth_id == auth_id)
        )

        return result.scalar_one_or_none()


    async def get_executor_profile(self, auth_id: int):
        result = await self.session.execute(
            select(ExecutorProfileModel).where(ExecutorProfileModel.auth_id == auth_id)
        )

        return result.scalar_one_or_none()

    async def get_task_by_id(self, task_id: int):
        result = await self.session.execute(select(TasksModel).where(TasksModel.id == task_id))
        return result.scalar_one_or_none()

    async def get_tasks_for_customer(self, user_id: int):
        result = await self.session.execute(select(TasksModel).where(TasksModel.user_id == user_id))
        return result.scalars()

    async def get_history_tasks(self, user_id: int):
        result = await self.session.execute(
            select(TasksModel).where(
                TasksModel.customer_id == user_id,
                TasksModel.status.notin_([TasksStatusEnum.CREATED, TasksStatusEnum.PROCESSING])
            )
        )
        return result.scalars()

    async def get_open_tasks(self, user_id: int):
        result = await self.session.execute(
            select(TasksModel).where(
                TasksModel.customer_id == user_id,
                TasksModel.status.notin_([TasksStatusEnum.CANCELLED, TasksStatusEnum.COMPLETED])
            )
        )
        return result.scalars()

    async def get_open_executor_tasks(self):
        result = await self.session.execute(
            select(TasksModel).where(
                TasksModel.status == TasksStatusEnum.CREATED
            )
        )
        return result.scalars()

    async def get_history_executor_tasks(self, user_id: int):
        result = await self.session.execute(
            select(TasksModel)
            .join(TaskResponseModel, TaskResponseModel.task_id == TasksModel.id)
            .where(TaskResponseModel.executor_id == user_id)
        )

        return result.scalars()

    async def get_role(self, role_id: int):
        result = await self.session.execute(
            select(RoleModel).where(RoleModel.id == role_id)
        )

        return result.scalar_one_or_none()


    async def create_task(self, model: TasksModel):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model


    async def update_task(self, model: TasksModel):
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def add_response_task(self, model: TaskResponseModel):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model


def get_tasks_repository(session: AsyncSession = Depends(get_session)) -> TasksRepository:
    return TasksRepository(session)
