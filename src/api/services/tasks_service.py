import json
import locale
from datetime import datetime, timedelta, timezone
import pytz
import aio_pika
from fastapi import Depends, HTTPException, BackgroundTasks
from firebase_admin import firestore
from starlette import status

from api.dto.tasks_dto import (TaskRequestDTO, TaskResponseDTO, CreateResponseTaskByIdDTO,
                               ResponseByTaskIdDTO, CustomerResponseDTO)
from api.firebase.utils import db
from api.repositories.tasks_repository import get_tasks_repository, TasksRepository
from core.config import settings
from models.entity import TasksModel, TaskResponseModel
from models.enums import RolesEnum, TasksStatusEnum, ResponseStatus
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
            taskStatus=self._formated_status(task.status),
            customer=CustomerResponseDTO(
                id=task.customer.id,
                firstName=task.customer.first_name,
                lastName=task.customer.last_name,
                photo=task.customer.photo
            )
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

                if not user_info:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Для начало заполните свой профиль",
                    )
                tasks = await self.tasks_repository.get_open_tasks(user_info.id)

            elif user_role.name == RolesEnum.EXECUTOR.value:

                executor_info = await self.tasks_repository.get_executor_profile(auth_id=auth_id)

                if not executor_info:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Для начало заполните свой профиль",
                    )

                tasks = await self.tasks_repository.get_open_executor_tasks(executor_info.id)

        if filters == 'history':

            if user_role.name == RolesEnum.CUSTOMER.value:

                user_info = await self.tasks_repository.get_customer_profile(auth_id=auth_id)
                if not user_info:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Для начало заполните свой профиль",
                    )
                tasks = await self.tasks_repository.get_history_tasks(user_info.id)

            elif user_role.name == RolesEnum.EXECUTOR.value:

                user_info = await self.tasks_repository.get_executor_profile(auth_id=auth_id)
                tasks = await self.tasks_repository.get_history_executor_tasks(user_info.id)

        if filters == 'open':
            if user_role.name == RolesEnum.EXECUTOR.value:
                user_info = await self.tasks_repository.get_executor_profile(auth_id=auth_id)

                if not user_info:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Для начало заполните свой профиль",
                    )

                tasks = await self.tasks_repository.get_open_tasks_for_executor(user_info.id)

                tasks_array = []

                for task in tasks:

                    if task.status == TasksStatusEnum.SEARCH:

                        firestore_task = await self.__search_task_in_firestore(task.id, user_info.id)

                        if firestore_task:
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
                                    roomUUID=task.responses.room_uuid,
                                    taskStatus=self._formated_status(task.status),
                                )
                            )
                    else:
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
                                roomUUID=task.responses.room_uuid,
                                taskStatus=self._formated_status(task.status),
                            )
                        )
                return tasks_array

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
                    roomUUID=task.responses.room_uuid if task.responses and task.responses.room_uuid else None,
                    taskStatus=self._formated_status(task.status),
                )
            )

        return tasks_array

    async def create_task(self, current_user: dict, data: TaskRequestDTO):
        auth_id = int(current_user.get('id'))
        user = await self.tasks_repository.get_customer_profile(auth_id=auth_id)

        if not user or not user.first_name or not user.last_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Для начало заполните профиль заказчика",
            )

        new_task = TasksModel(
            name=data.taskName,
            description=data.taskDescription,
            price=data.taskPrice,
            term_to=data.taskTerm.replace(tzinfo=None),
            term_from=datetime.utcnow(),
            location=data.taskCity,
            is_public=True,
            customer_id=user.id,
            status=TasksStatusEnum.SEARCH
        )

        task = await self.tasks_repository.create_task(new_task)

        await self._send_to_rabbitmq(
            {
                "task_id": task.id,
                "title": task.name,
                "body": task.description,
                "image": "http://31.129.108.27:9000/photos/default/Logo.png"
            }
        )

        return TaskResponseDTO(
            id=task.id,
            taskName=task.name,
            taskDescription=task.description,
            taskPrice=task.price,
            taskTerm=self.__format_date(task.term_to),
            taskCity=task.location,
            isPublic=task.is_public,
            taskStatus=self._formated_status(task.status),
            taskCreated=self.__format_date(task.term_from),
            customer=CustomerResponseDTO(
                id=user.id,
                firstName=user.first_name,
                lastName=user.last_name,
                photo=user.photo
            )
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
            taskStatus=self._formated_status(task_update.status),
            taskCreated=self.__format_date(task_update.term_from),
        )

    async def response_task_by_id(self, task_id: int, current_user: dict, data: CreateResponseTaskByIdDTO,
                                  background_task: BackgroundTasks):
        """
        Создание отклика, комнаты и сообщения в Firebase Firestore.
        """
        auth_id = int(current_user.get('id'))
        task = await self.tasks_repository.get_task_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )

        executor = await self.tasks_repository.get_executor_profile(auth_id=auth_id)

        if not executor.first_name or not executor.last_name:
            raise HTTPException(
                detail="Для начала заполните анкету",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        existing_response = await self.tasks_repository.existing_response(task.id, executor.id)

        if existing_response:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Отклик уже отправлен"
            )

        new_response = TaskResponseModel(
            task_id=task_id,
            executor_id=executor.id,
            text=data.text,
            status=ResponseStatus.EXPECTATION
        )

        await self.tasks_repository.create_task_response(new_response)

        background_task.add_task(
            self.__create_room_and_message,
            task=task,
            executor=executor,
            data=data,
            response=new_response
        )

        return {"message": "Отклик успешно отправлен, комната создается в фоне"}


    async def get_response_by_task_id(self, task_id: int, current_user: dict):
        task = await self.tasks_repository.get_task_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found'
            )

        task_response = await self.tasks_repository.get_response_by_task_id(task_id=task_id)

        response_array = []

        for response in task_response:

            positive, negative = await self.tasks_repository.get_executor_review_counts(response.executor.id)

            response_array.append(
                ResponseByTaskIdDTO(
                    id=response.id,
                    firstName=response.executor.first_name,
                    lastName=response.executor.last_name,
                    photo=response.executor.photo,
                    created_at=self.__get_date_description(response.response_date),
                    text=response.text,
                    rating=positive,
                    roomUUID=response.room_uuid
                )
            )

        return response_array

    async def response_executor_by_task_id(self, task_id: int, response_id: int, current_user: dict):
        response = await self.tasks_repository.get_response_by_id(response_id=response_id, task_id=task_id)

        if not response:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Данный отклик на данную задачу не найдено"
            )

        await self.tasks_repository.update_response_status(task_id=task_id, response_id=response_id)
        return {"message": "Вы назначены исполнителем"}

    async def done_task_by_id_service(self, task_id: int, current_user: dict):
        response = await self.tasks_repository.get_task_response_by_id(task_id)

        if not response:
            raise HTTPException(
                detail="Task not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        response.task.status = TasksStatusEnum.COMPLETED


        await self.tasks_repository.update_response_task_model(response)

        return {"message": "Задача выполнена"}

    async def send_review_task_by_id(self, task_id: int, current_user: dict):
        response = await self.tasks_repository.get_task_response_by_id(task_id)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        response.task.status = TasksStatusEnum.UNDER_REVIEW
        await self.tasks_repository.update_response_task_model(response)

        return {"message": "Задание отправлено на проверку"}


    def __get_date_description(self, input_datetime: datetime) -> str:
        now = datetime.now()
        today = now.date()
        yesterday = today - timedelta(days=1)
        day_before_yesterday = today - timedelta(days=2)

        input_date = input_datetime.date()

        if input_date == today:
            return "сегодня"
        elif input_date == yesterday:
            return "вчера"
        elif input_date == day_before_yesterday:
            return "позавчера"
        else:
            return input_datetime.strftime("%d %B %Y")

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

    def _formated_status(self, status: str) -> str:
        if status == TasksStatusEnum.WORK:
            return "В работе"
        elif status == TasksStatusEnum.SEARCH:
            return "Поиск исполнителя"
        elif status == TasksStatusEnum.COMPLETED:
            return "Завершено"
        elif status == TasksStatusEnum.CANCELLED:
            return "Отменено"
        else:
            return "Неизвестный статус"

    async def __search_task_in_firestore(self, task_id: int, executor_id: int):
        rooms_ref = db.collection("rooms")
        query = (
            rooms_ref
            .where("task_id", "==", task_id)
            .where("executor_id", "==", executor_id)
            .where("is_response", "==", False)  # Фильтр по is_response
        )
        docs = query.stream()

        return any(docs)


    async def __create_room_and_message(self, task, executor, data, response):
        """
        Создание комнаты и сообщения в Firebase Firestore.
        """
        rooms_ref = db.collection("rooms")

        # Создание комнаты
        new_room_data = {
            "name": task.name,
            "task_id": task.id,
            "executor_id": executor.id,
            "customer_id": task.customer_id,
            "response_id": response.id,
            "created_at": firestore.firestore.SERVER_TIMESTAMP,
            "is_response": True, # если true, то это отклик если false, то уже переписка
        }
        new_room_ref = rooms_ref.document()
        new_room_ref.set(new_room_data)

        # Создание сообщения
        messages_ref = new_room_ref.collection("messages")
        new_message_data = {
            "senderId": executor.id,  # Автор сообщения — исполнитель
            "content": data.text,
            "created_at": firestore.firestore.SERVER_TIMESTAMP,
        }
        new_message_ref = messages_ref.document()
        new_message_ref.set(new_message_data)

        # Обновление room_uuid в TaskResponseModel
        response.room_uuid = new_room_ref.id
        await self.tasks_repository.update_task_response(response)

    async def _send_to_rabbitmq(self, message: dict):
        try:
            connection = await aio_pika.connect_robust("amqp://workers_rabbitmq:5672")

            # Открываем канал в асинхронном контексте
            async with connection:
                channel = await connection.channel()

                # Объявление очереди
                await channel.declare_queue("notifications", durable=True)

                # Отправка сообщения в очередь
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(message).encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # Сообщение сохраняется на диске
                    ),
                    routing_key="notifications",
                )

        except Exception as e:
            print(e)

def get_tasks_service(tasks_repository: TasksRepository = Depends(get_tasks_repository)):
    return TasksService(tasks_repository)
