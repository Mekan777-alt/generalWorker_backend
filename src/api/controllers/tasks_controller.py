from fastapi import Depends, APIRouter
from sqlalchemy.testing.pickleable import User
from starlette import status
from typing import Annotated, List
from api.dependency.current_user import get_user_from_token
from api.dto.tasks_dto import TaskRequestDTO, TaskResponseDTO
from api.services.tasks_service import get_tasks_service, TasksService

router = APIRouter(
    tags=['Задачи']
)

@router.get('/tasks',
            summary="Возвращает массив задач по текущему заказчику",
            status_code=status.HTTP_200_OK,
            response_model=List[TaskResponseDTO])
async def get_tasks(current_user: Annotated[dict, Depends(get_user_from_token)],
                    service: TasksService = Depends(get_tasks_service)):
    return await service.get_tasks_for_customer(current_user)

@router.post('/tasks',
             summary="Создать задачу",
             status_code=status.HTTP_201_CREATED,
             response_model=TaskResponseDTO
             )
async def create_task_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                               data: TaskRequestDTO,
                               service: TasksService = Depends(get_tasks_service)):
    return await service.create_task(current_user, data)


@router.patch('/tasks/{task_id}',
              summary="Обновление задачи",
              status_code=status.HTTP_200_OK,
              response_model=TaskResponseDTO
              )
async def update_task_endpoint(task_id: int,
                               current_user: Annotated[dict, Depends(get_user_from_token)],
                               data: TaskRequestDTO,
                               service: TasksService = Depends(get_tasks_service)
                               ):
    return await service.update_task(task_id, data)


@router.post('/tasks/{task_id}/confirm',
             summary="Подтверждение публикации задания",
             status_code=status.HTTP_201_CREATED,
             response_model=TaskResponseDTO
             )
async def confirm_task_endpoint(task_id: int,
                                current_user: Annotated[dict, Depends(get_user_from_token)],
                                service: TasksService = Depends(get_tasks_service)
                                ):
    return await service.confirm_task(task_id)