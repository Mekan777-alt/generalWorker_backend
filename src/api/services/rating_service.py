from fastapi import Depends
from api.repositories.rating_repository import get_rating_repository, RatingRepository
from api.repositories.tasks_repository import get_tasks_repository, TasksRepository
from models.enums import RolesEnum

class RatingService:
    def __init__(self, rating_repository: RatingRepository, tasks_repository: TasksRepository):
        self.rating_repository = rating_repository
        self.tasks_repository = tasks_repository


    async def get_rating_current_user(self, current_user: dict):
        auth_id = current_user.get('id')
        role_id = current_user.get('role_id')

        user_role = await self.rating_repository.get_role_by_id(role_id)

        if user_role.name == RolesEnum.CUSTOMER.value:
            customer_profile = await self.tasks_repository.get_customer_profile(auth_id)

            positive, negative = await self.tasks_repository.get_customer_review_counts(customer_profile.id)

            tasks_count = await self.tasks_repository.get_tasks_count_by_customer_id(customer_profile.id)

            return {
                'positive': positive,
                'negative': negative,
                'tasks_count': tasks_count
            }

        if user_role.name == RolesEnum.EXECUTOR.value:
            executor_profile = await self.tasks_repository.get_executor_profile(auth_id)

            positive, negative = await self.tasks_repository.get_executor_review_counts(executor_profile.id)



def get_rating_service(rating_repository: RatingRepository = Depends(get_rating_repository),
                       tasks_repository: TasksRepository = Depends(get_tasks_repository)) -> RatingService:
    return RatingService(rating_repository=rating_repository, tasks_repository=tasks_repository)
