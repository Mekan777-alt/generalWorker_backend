import asyncio
import json
import os

import aio_pika
import firebase_admin
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.session import async_session_maker
from firebase_admin import messaging, credentials
from models.entity import TasksModel, UserProfileModel, UserRolesModel, RoleModel


# Функция для отправки уведомления
async def send_notification(token: str, title: str, body: str, image: str, task_id: int):
    message = messaging.Message(
        token=token,
        data={
            "title": title,
            "body": body,
            "image": image,
            "task_id": str(task_id)  # Firebase ожидает строки
        },
        notification=messaging.Notification(
            title=title,
            body=body,
        )
    )

    messaging.send(message)


# Функция для получения задачи по ID
async def get_task_by_id(task_id: int, session: AsyncSession):
    result = await session.execute(
        select(TasksModel)
        .where(TasksModel.id == task_id)
    )
    return result.scalar_one_or_none()


# Асинхронный callback для обработки сообщений
async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            async with async_session_maker() as session:
                msg_body = json.loads(message.body.decode())
                print(f"Сообщение: {msg_body}")

                task = await get_task_by_id(msg_body["task_id"], session)
                print(f"{task.id} - name: {task.name} найдена")
                if task:
                    users = await get_executors_by_city(task.location, session)
                    for user in users:
                        await send_notification(
                            token=user.get('executor_token'),
                            title=msg_body["title"],
                            body=msg_body["body"],
                            image=msg_body["image"],
                            task_id=msg_body["task_id"]
                        )
                else:
                    print(f"Task with ID {msg_body['task_id']} not found.")
        except Exception as e:
            print(f"Error processing message: {str(e)}")


async def get_executors_by_city(city: str, session: AsyncSession):
    result = await session.execute(
        select(UserProfileModel)
        .join(UserProfileModel.user_roles)
        .join(UserRolesModel.role)
        .options(
            joinedload(UserProfileModel.user_roles)
            .joinedload(UserRolesModel.role)
        )
        .where(UserProfileModel.location == city)
        .where(RoleModel.name == 'Executor')
    )
    executors = result.scalars().unique().all()

    result_list = []
    for user in executors:
        executor_role = next(
            (ur for ur in user.user_roles if ur.role and ur.role.name == 'Executor'),
            None
        )
        token = executor_role.token if executor_role else None

        result_list.append({
            "user": user,            # Сам объект UserProfileModel
            "executor_token": token  # Его токен именно для роли Executor
        })

    return result_list


# Функция для запуска асинхронного worker
async def start_worker():
    try:
        connection = await aio_pika.connect_robust("amqp://workers_rabbitmq:5672")
        print("Connected to RabbitMQ")
        channel = await connection.channel()

        # Объявление очереди
        queue = await channel.declare_queue("notifications", durable=True)

        # Настройка потребителя
        await queue.consume(callback)

        await asyncio.Future()  # Бесконечное ожидание сообщений
    except Exception as e:
        print(f"Worker failed: {str(e)}")


if __name__ == "__main__":
    cred = credentials.Certificate(f"{os.getcwd()}/app-freelance-f3dee-firebase-adminsdk-8d92q-f8deea39b3.json")
    firebase_admin.initialize_app(cred)
    print("Connected to Firebase")
    asyncio.run(start_worker())