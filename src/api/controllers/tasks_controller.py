from fastapi import Depends, APIRouter
from starlette import status

from api.services.tasks_service import get_tasks_service, TasksService

router = APIRouter(
    tags=['Задачи'],
    prefix='/api',
)

@router.get('/tasks', summary="Возвращает массив задач для исполнителя", status_code=status.HTTP_200_OK)
async def get_tasks(service: TasksService = Depends(get_tasks_service)):
    pass