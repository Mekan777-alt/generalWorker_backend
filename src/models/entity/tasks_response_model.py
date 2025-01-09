from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.base import Base
from models.enums import TaskResponseStatusEnum

class TaskResponseModel(Base):
    __tablename__ = 'task_responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    executor_id = Column(Integer, ForeignKey('user_profile.id', ondelete='CASCADE'), nullable=False)  # Унифицированный профиль
    status = Column(Enum(TaskResponseStatusEnum), default=TaskResponseStatusEnum.PENDING, nullable=False)
    text = Column(String, nullable=True)
    response_date = Column(DateTime, default=datetime.utcnow)
    room_uuid = Column(String, nullable=True)

    task = relationship("TasksModel", back_populates="responses")
    executor = relationship("UserProfileModel", back_populates="responses")
