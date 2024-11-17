from sqlalchemy import select, func, case
from sqlalchemy.orm import joinedload

from models.enums import TasksStatusEnum
from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from models.entity import TasksModel, RoleModel, CustomerProfileModel, ExecutorProfileModel, TaskResponseModel, \
    ReviewModel


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

    async def get_response_by_task_id(self, task_id: int):
        result = await self.session.execute(
            select(TaskResponseModel)
            .options(joinedload(TaskResponseModel.executor))
            .where(TaskResponseModel.task_id == task_id)
        )
        return result.scalars().all()

    async def get_executor_review_counts(self, executor_id: int):
        """
        Подсчет количества положительных и отрицательных отзывов исполнителя.
        """
        result = await self.session.execute(
            select(
                func.sum(
                    case((ReviewModel.rating == True, 1), else_=0)
                ).label('positive_reviews'),
                func.sum(
                    case((ReviewModel.rating == False, 1), else_=0)
                ).label('negative_reviews')
            ).where(ReviewModel.executor_id == executor_id)
        )
        positive_reviews, negative_reviews = result.one_or_none()

        return positive_reviews or 0, negative_reviews or 0

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
