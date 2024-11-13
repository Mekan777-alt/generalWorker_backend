from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from starlette import status
from api.dto.tasks_dto import TaskRequestDTO, TaskResponseDTO
from api.repositories.tasks_repository import get_tasks_repository, TasksRepository
from models.entity import TasksModel

class TasksService:
    def __init__(self, tasks_repository: TasksRepository):
        self.tasks_repository = tasks_repository

    async def get_tasks_for_customer(self, current_user: dict):
        auth_id = int(current_user.get('id'))
        user = await self.tasks_repository.get_user(auth_id=auth_id)

        tasks = await self.tasks_repository.get_tasks_for_customer(user.id)
        tasks_array = []

        for task in tasks:
            tasks_array.append(
                TaskResponseDTO(
                    id=task.id,
                    taskName=task.name,
                    taskDescription=task.description,
                    taskPrice=task.price,
                    taskTerm=task.term_to,
                    taskCity=task.location,
                    isPublic=task.is_public
                )
            )

        return tasks_array

    async def create_task(self, current_user: dict, data: TaskRequestDTO):
        auth_id = int(current_user.get('id'))
        user = await self.tasks_repository.get_user(auth_id=auth_id)

        new_task = TasksModel(
            name=data.taskName,
            description=data.taskDescription,
            price=data.taskPrice,
            term_to=data.taskTerm.replace(tzinfo=None),
            term_from=datetime.utcnow(),
            location=data.taskCity,
            user_id=user.id
        )

        await self.tasks_repository.create_task(new_task)

        return TaskResponseDTO(
            id=new_task.id,
            taskName=new_task.name,
            taskDescription=new_task.description,
            taskPrice=new_task.price,
            taskTerm=new_task.term_to,
            taskCity=new_task.location,
            isPublic=new_task.is_public
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

def get_tasks_service(tasks_repository: TasksRepository = Depends(get_tasks_repository)):
    return TasksService(tasks_repository)
