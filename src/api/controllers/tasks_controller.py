from fastapi import Depends, APIRouter, Query, BackgroundTasks
from starlette import status
from typing import Annotated, List
from api.dependency.current_user import get_user_from_token
from api.dto.tasks_dto import TaskRequestDTO, TaskResponseDTO, TaskRequestDescriptionDTO, CreateResponseTaskByIdDTO
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
                                                  description="Фильтры для задач, например 'tasks,history,open'"),
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
             summary="Отправка отклика на вакансию",
             status_code=status.HTTP_201_CREATED,
             )
async def response_task_endpoint(task_id: int,
                                 background_task: BackgroundTasks,
                                 data: CreateResponseTaskByIdDTO,
                                 current_user: Annotated[dict, Depends(get_user_from_token)],
                                 service: TasksService = Depends(get_tasks_service),
                                 ):
    return await service.response_task_by_id(task_id, current_user, data, background_task)

@router.get('/tasks/{task_id}/response',
            summary="Возвращает массив откликов на данную задачу",
            status_code=status.HTTP_200_OK
            )
async def get_response_task_endpoint(task_id: int,
                                     current_user: Annotated[dict, Depends(get_user_from_token)],
                                     service: TasksService = Depends(get_tasks_service)):
    return await service.get_response_by_task_id(task_id, current_user)


@router.post('/tasks/{task_id}/response/{response_id}',
            summary="Назначение исполнителя по данной задаче",
            status_code=status.HTTP_200_OK
            )
async def response_task_by_response_id_endpoint(task_id: int,
                                                    response_id: int,
                                                    current_user: Annotated[dict, Depends(get_user_from_token)],
                                                    service: TasksService = Depends(get_tasks_service)):
    return await service.response_executor_by_task_id(task_id, response_id, current_user)


@router.post('/tasks/{task_id}/review',
             status_code=status.HTTP_200_OK,
             summary="Отправка на проверку",
            )
async def send_review_from_executor_endpoint(task_id: int,
                                             current_user: Annotated[dict, Depends(get_user_from_token)],
                                             service: TasksService = Depends(get_tasks_service)):
    return await service.send_review_task_by_id(task_id, current_user)


@router.post('/tasks/{task_id}/done',
             summary="Подтверждение задачи на статус ВЫПОЛНЕНО",
             status_code=status.HTTP_200_OK
             )
async def done_workflow_endpoint(task_id: int,
                                 current_user: Annotated[dict, Depends(get_user_from_token)],
                                 service: TasksService = Depends(get_tasks_service)):
    return await service.done_task_by_id_service(task_id, current_user)
