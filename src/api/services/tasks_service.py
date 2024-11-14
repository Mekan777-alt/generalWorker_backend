import locale

from datetime import datetime, timezone

from models.enums import TasksStatusEnum
from fastapi import Depends, HTTPException
from starlette import status
from api.dto.tasks_dto import TaskRequestDTO, TaskResponseDTO, TaskRequestDescriptionDTO
from api.repositories.tasks_repository import get_tasks_repository, TasksRepository
from models.entity import TasksModel
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


    async def get_tasks_for_customer(self, current_user: dict, filters: str):
        auth_id = int(current_user.get('id'))
        user = await self.tasks_repository.get_user(auth_id=auth_id)
        tasks = None

        tasks_array = []

        if filters == 'open':
            tasks = await self.tasks_repository.get_open_tasks(user.id)

        if filters == 'history':
            tasks = await self.tasks_repository.get_history_tasks(user.id)


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
        user = await self.tasks_repository.get_user(auth_id=auth_id)

        new_task = TasksModel(
            name=data.taskName,
            price=data.taskPrice,
            term_to=data.taskTerm.replace(tzinfo=None),
            term_from=datetime.utcnow(),
            location=data.taskCity,
            user_id=user.id,
            status=TasksStatusEnum.CREATED
        )

        await self.tasks_repository.create_task(new_task)

        return TaskResponseDTO(
            id=new_task.id,
            taskName=new_task.name,
            taskPrice=new_task.price,
            taskTerm=new_task.term_to,
            taskCity=new_task.location,
            isPublic=new_task.is_public
        )

    async def update_task_to_description(self, task_id: int, data: TaskRequestDescriptionDTO):
        task = await self.tasks_repository.get_task_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )

        task.description = data.taskDescription

        await self.tasks_repository.update_task(task)

        return TaskResponseDTO(
            id=task.id,
            taskName=task.name,
            taskDescription=task.description,
            taskPrice=task.price,
            taskTerm=task.term_to,
            taskCity=task.location,
            isPublic=task.is_public
        )


    async def update_task(self, task_id: int, data: TaskRequestDTO):
        task = await self.tasks_repository.get_task_by_id(task_id)

        if task is None:

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

        await self.tasks_repository.update_task(task)

        return TaskResponseDTO(
            id=task.id,
            taskName=task.name,
            taskDescription=task.description,
            taskPrice=task.price,
            taskTerm=task.term_to,
            taskCity=task.location,
            isPublic=task.is_public
        )

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
