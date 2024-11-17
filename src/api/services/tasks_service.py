import locale
from datetime import datetime
from models.enums import TasksStatusEnum
from fastapi import Depends, HTTPException
from starlette import status
from api.dto.tasks_dto import TaskRequestDTO, TaskResponseDTO, TaskRequestDescriptionDTO
from api.repositories.tasks_repository import get_tasks_repository, TasksRepository
from models.entity import TasksModel, TaskResponseModel
from models.enums import RolesEnum
from babel.dates import format_date

class TasksService:
    def __init__(self, tasks_repository: TasksRepository):
        self.tasks_repository = tasks_repository

    async def get_task_by_id(self, task_id: int) -> TaskResponseDTO:
        task = await self.tasks_repository.get_task_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return TaskResponseDTO(
            id=task.id,
            taskName=task.name,
            taskDescription=task.description,
            taskPrice=task.price,
            taskTerm=self.__format_duration(task.term_from, task.term_to),
            taskCreated=self.__format_date(task.term_from),
            taskCity=task.location,
            isPublic=task.is_public,
            taskStatus=task.status
        )


    async def get_tasks_for_all_user(self, current_user: dict, filters: str):
        auth_id = int(current_user.get('id'))
        role_id = int(current_user.get('role_id'))

        user_role = await self.tasks_repository.get_role(role_id=role_id)

        tasks = None
        tasks_array = []

        if filters == 'tasks':

            if user_role.name == RolesEnum.CUSTOMER.value:

                user_info = await self.tasks_repository.get_customer_profile(auth_id=auth_id)
                tasks = await self.tasks_repository.get_open_tasks(user_info.id)

            elif user_role.name == RolesEnum.EXECUTOR.value:

                tasks = await self.tasks_repository.get_open_executor_tasks()

        if filters == 'history':

            if user_role.name == RolesEnum.CUSTOMER.value:

                user_info = await self.tasks_repository.get_customer_profile(auth_id=auth_id)
                tasks = await self.tasks_repository.get_history_tasks(user_info.id)

            elif user_role.name == RolesEnum.EXECUTOR.value:

                user_info = await self.tasks_repository.get_executor_profile(auth_id=auth_id)
                tasks = await self.tasks_repository.get_history_executor_tasks(user_info.id)

        if not tasks:

            return []

        for task in tasks:
            tasks_array.append(
                TaskResponseDTO(
                    id=task.id,
                    taskName=task.name,
                    taskDescription=task.description,
                    taskPrice=task.price,
                    taskTerm=self.__format_duration(task.term_from, task.term_to),
                    taskCreated=self.__format_date(task.term_from),
                    taskCity=task.location,
                    isPublic=task.is_public,
                    taskStatus=task.status
                )
            )

        return tasks_array

    async def create_task(self, current_user: dict, data: TaskRequestDTO):
        auth_id = int(current_user.get('id'))
        user = await self.tasks_repository.get_customer_profile(auth_id=auth_id)

        new_task = TasksModel(
            name=data.taskName,
            description=data.taskDescription,
            price=data.taskPrice,
            term_to=data.taskTerm.replace(tzinfo=None),
            term_from=datetime.utcnow(),
            location=data.taskCity,
            customer_id=user.id,
            status=TasksStatusEnum.CREATED
        )

        task = await self.tasks_repository.create_task(new_task)

        return TaskResponseDTO(
            id=task.id,
            taskName=task.name,
            taskDescription=task.description,
            taskPrice=task.price,
            taskTerm=self.__format_date(task.term_to),
            taskCity=task.location,
            isPublic=task.is_public,
            taskStatus=task.status,
            taskCreated=self.__format_date(task.term_from),
        )

    async def update_task_to_description(self, task_id: int, data: TaskRequestDescriptionDTO):
        task = await self.tasks_repository.get_task_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )

        task.description = data.taskDescription

        task_update = await self.tasks_repository.update_task(task)

        return TaskResponseDTO(
            id=task_update.id,
            taskName=task_update.name,
            taskDescription=task_update.description,
            taskPrice=task_update.price,
            taskTerm=self.__format_date(task_update.term_to),
            taskCity=task_update.location,
            isPublic=task_update.is_public,
            taskStatus=task_update.status,
            taskCreated=self.__format_date(task_update.term_from),
        )


    async def update_task(self, task_id: int, data: TaskRequestDTO):
        task = await self.tasks_repository.get_task_by_id(task_id)

        if not task:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )

        if data.taskName:
            task.name = data.taskName
        if data.taskDescription:
            task.description = data.taskDescription
        if data.taskPrice:
            task.price = data.taskPrice
        if data.taskTerm:
            task.term_to = data.taskTerm.replace(tzinfo=None)
        if data.taskCity:
            task.location = data.taskCity

        updating_task = await self.tasks_repository.update_task(task)

        return TaskResponseDTO(
            id=updating_task.id,
            taskName=updating_task.name,
            taskDescription=updating_task.description,
            taskPrice=updating_task.price,
            taskTerm=updating_task.term_to,
            taskCity=updating_task.location,
            isPublic=updating_task.is_public
        )

    async def confirm_task(self, task_id: int):
        task = await self.tasks_repository.get_task_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )

        task.is_public = True

        task_update = await self.tasks_repository.update_task(task)

        return TaskResponseDTO(
            id=task_update.id,
            taskName=task_update.name,
            taskDescription=task_update.description,
            taskPrice=task_update.price,
            taskTerm=self.__format_date(task_update.term_to),
            taskCity=task_update.location,
            isPublic=task_update.is_public,
            taskStatus=task_update.status,
            taskCreated=self.__format_date(task_update.term_from),
        )

    async def response_task_by_id(self, task_id: int, current_user: dict):
        auth_id = int(current_user.get('id'))
        task = await self.tasks_repository.get_task_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )

        executor = await self.tasks_repository.get_executor_profile(auth_id=auth_id)

        if not executor:

            raise HTTPException(
                detail="Для начало заполните анкету",
                status_code=status.HTTP_404_NOT_FOUND
            )

        new_response = TaskResponseModel(
            task_id=task_id,
            executor_id=executor.id
        )

        await self.tasks_repository.add_response_task(new_response)

        return {"message": "Отклик на задачу успешно добавлен"}

    def __format_duration(self, term_from, term_to):
        # Рассчитываем разницу между датами
        duration = term_to - term_from

        # Получаем дни и оставшиеся часы
        days = duration.days
        hours = duration.seconds // 3600

        if days > 0:
            return f"{days} дней {hours} часов" if hours > 0 else f"{days} дней"
        else:
            return f"{hours} часов"

    def __format_date(self, date: datetime) -> str:
        # Убедитесь, что локаль установлена на русский
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # Форматируем дату с русским названием месяца
        return format_date(date, format="d MMMM yyyy", locale='ru')

def get_tasks_service(tasks_repository: TasksRepository = Depends(get_tasks_repository)):
    return TasksService(tasks_repository)
