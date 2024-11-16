from fastapi import Depends, APIRouter, Query
from starlette import status
from typing import Annotated, List
from api.dependency.current_user import get_user_from_token
from api.dto.tasks_dto import TaskRequestDTO, TaskResponseDTO, TaskRequestDescriptionDTO
from api.services.tasks_service import get_tasks_service, TasksService

router = APIRouter(
    tags=['Задачи для заказчика']
)

@router.get('/tasks',
            summary="Возвращает массив задач для всех вид роль",
            status_code=status.HTTP_200_OK,
            response_model=List[TaskResponseDTO]
            )
async def get_tasks_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                             filters: str = Query("tasks",
                                                  description="Фильтры для задач, например 'tasks,history'"),
                             service: TasksService = Depends(get_tasks_service)):
    return await service.get_tasks_for_all_user(current_user, filters)


@router.get('/tasks/{task_id}',
            summary="Возвращает задачу по ID",
            status_code=status.HTTP_200_OK,
            response_model=TaskResponseDTO
            )
async def get_task_by_id_endpoint(task_id: int,
                                  current_user: Annotated[dict, Depends(get_user_from_token)],
                                  service: TasksService = Depends(get_tasks_service)):
    return await service.get_task_by_id(task_id)

@router.post('/tasks',
             summary="Создать задачу",
             status_code=status.HTTP_201_CREATED,
             response_model=TaskResponseDTO
             )
async def create_task_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                               data: TaskRequestDTO,
                               service: TasksService = Depends(get_tasks_service)):
    return await service.create_task(current_user, data)

@router.post('/tasks/{task_id}/description',
             summary="Добавление описании задачи",
             status_code=status.HTTP_201_CREATED,
             response_model=TaskResponseDTO
             )
async def create_task_description_endpoint(task_id: int,
                                           current_user: Annotated[dict, Depends(get_user_from_token)],
                                           data: TaskRequestDescriptionDTO,
                                           service: TasksService = Depends(get_tasks_service)):
    return await service.update_task_to_description(task_id, data)


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

@router.post('/tasks/{task_id}/response',
             summary="Отклик на вакансию",
             status_code=status.HTTP_201_CREATED,
             )
async def response_task_endpoint(task_id: int,
                                 current_user: Annotated[dict, Depends(get_user_from_token)],
                                 service: TasksService = Depends(get_tasks_service)):
    return await service.response_task_by_id(task_id, current_user)