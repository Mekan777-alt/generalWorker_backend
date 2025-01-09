
from sqlalchemy import select, func, case, update, not_
from sqlalchemy.orm import joinedload
from models.enums import TasksStatusEnum, TaskResponseStatusEnum
from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from models.entity import TasksModel, RoleModel, TaskResponseModel, \
    ReviewModel, UserProfileModel


class TasksRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def customer_create_task_count(self, customer_id: int):
        result = await self.session.execute(
            select(func.count(TasksModel.id))
            .where(TasksModel.customer_id == customer_id)
        )
        return result.scalar() or 0

    async def completed_task_count_executor(self, executor_id: int):
        result = await self.session.execute(
            select(func.count(TaskResponseModel.id))
            .where(
                TaskResponseModel.executor_id == executor_id,
                TasksModel.status == TasksStatusEnum.COMPLETED
            )
        )
        return result.scalar() or 0

    async def total_earning_executor(self, executor_id: int):
        result = await self.session.execute(
            select(func.sum(TasksModel.price))
            .join(TaskResponseModel, TaskResponseModel.task_id == TasksModel.id)
            .where(
                TaskResponseModel.executor_id == executor_id,
                TasksModel.status == TasksStatusEnum.COMPLETED
            )
        )
        return result.scalar() or 0

    async def review_executor(self, executor_id: int):
        reviews_query = await self.session.execute(
            select(
                ReviewModel.comment,
                ReviewModel.rating,
                ReviewModel.created_at,
                UserProfileModel.first_name,
                UserProfileModel.photo
            )
            .join(UserProfileModel, ReviewModel.customer_id == UserProfileModel.id)
            .where(ReviewModel.executor_id == executor_id)
            .order_by(ReviewModel.created_at.desc())
        )
        return reviews_query.fetchall()

    async def get_customer_profile(self, auth_id: int):
        result = await self.session.execute(
            select(UserProfileModel)
            .where(UserProfileModel.auth_id == auth_id)
        )

        return result.scalar_one_or_none()

    async def get_executor_profile(self, auth_id: int):
        result = await self.session.execute(
            select(UserProfileModel)
            .where(UserProfileModel.auth_id == auth_id)
        )

        return result.scalar_one_or_none()

    async def existing_response(self, task_id: int, executor_id: int):
        result = await self.session.execute(
            select(TaskResponseModel).where(
                TaskResponseModel.task_id == task_id,
                TaskResponseModel.executor_id == executor_id
            )
        )
        return result.scalar_one_or_none()

    async def get_task_by_id(self, task_id: int):
        result = await self.session.execute(
            select(TasksModel)
            .options(joinedload(TasksModel.customer))
            .where(TasksModel.id == task_id))
        return result.scalar_one_or_none()

    async def create_task_response(self, model: TaskResponseModel):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_response_by_task_id(self, task_id: int):
        result = await self.session.execute(
            select(TaskResponseModel)
            .options(joinedload(TaskResponseModel.executor))
            .where(TaskResponseModel.task_id == task_id)
        )
        return result.scalars().all()

    async def get_response_by_id(self, response_id: int, task_id: int):
        result = await self.session.execute(
            select(TaskResponseModel).where(TaskResponseModel.id == response_id,
                                            TaskResponseModel.task_id == task_id)
        )
        return result.scalar_one_or_none()

    async def update_response_status(self, response_id: int, task_id: int):
        # Обновить выбранный response на ACCEPTED
        accept_query = (
            update(TaskResponseModel)
            .where(TaskResponseModel.id == response_id, TaskResponseModel.task_id == task_id)
            .values(status=TaskResponseStatusEnum.ACCEPTED)
        )
        await self.session.execute(accept_query)

        # Обновить все остальные response того же task_id на REJECTED
        reject_query = (
            update(TaskResponseModel)
            .where(TaskResponseModel.task_id == task_id, TaskResponseModel.id != response_id)
            .values(status=TaskResponseStatusEnum.REJECTED)
        )
        await self.session.execute(reject_query)

        # Сохранить изменения
        await self.session.commit()

    async def update_task_status(self, task_id: int):

        query = (
            update(TasksModel)
            .where(TasksModel.id == task_id)
            .values(status=TasksStatusEnum.PROCESSING)
        )
        await self.session.execute(query)

        await self.session.commit()


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

    async def get_customer_review_counts(self, customer_id: int):
        """
        Подсчет количества положительных и отрицательных отзывов заказчика.
        """
        result = await self.session.execute(
            select(
                func.sum(
                    case((ReviewModel.rating == True, 1), else_=0)
                ).label('positive_reviews'),
                func.sum(
                    case((ReviewModel.rating == False, 1), else_=0)
                ).label('negative_reviews')
            ).where(ReviewModel.customer_id == customer_id)
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

    async def get_tasks_count_by_customer_id(self, customer_id: int):
        result = await self.session.execute(
            select(func.count(TasksModel)).where(TasksModel.customer_id == customer_id)
        )

        return result.scalar_one_or_none()

    async def get_open_tasks(self, user_id: int):
        result = await self.session.execute(
            select(TasksModel)
            .where(
                TasksModel.customer_id == user_id,
                TasksModel.status.notin_([TasksStatusEnum.CANCELLED, TasksStatusEnum.COMPLETED])
            )
        )
        return result.scalars()

    async def get_open_tasks_for_executor(self, executor_id: int):
        result = await self.session.execute(
            select(TaskResponseModel)
            .options(joinedload(TaskResponseModel.task))
            .where(
                TaskResponseModel.executor_id == executor_id,
            )
        )
        return result.scalars().all()

    async def get_open_executor_tasks(self, executor_id: int):
        subquery = select(TaskResponseModel.task_id).where(TaskResponseModel.executor_id == executor_id)
        result = await self.session.execute(
            select(TasksModel)
            .where(
                TasksModel.status == TasksStatusEnum.CREATED,
                not_(TasksModel.id.in_(subquery))
            )
        )
        return result.scalars().all()

    async def get_history_executor_tasks(self, user_id: int):
        result = await self.session.execute(
            select(TasksModel)
            .join(TaskResponseModel, TaskResponseModel.task_id == TasksModel.id)
            .where(TaskResponseModel.executor_id == user_id,
                   TasksModel.status.in_([TasksStatusEnum.COMPLETED, TasksStatusEnum.CANCELLED])
            )
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
