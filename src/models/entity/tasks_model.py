from datetime import datetime

from sqlalchemy import Column, String, Integer, NUMERIC, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from models.enums import TasksStatusEnum
from src.database.base import Base

class TasksModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(NUMERIC, nullable=False)
    term_from = Column(DateTime, nullable=False, default=datetime.utcnow)
    term_to = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    is_public = Column(Boolean, default=False)
    status = Column(Enum(TasksStatusEnum), default=TasksStatusEnum.SEARCH)
    customer_id = Column(Integer, ForeignKey('user_profile.id', ondelete='CASCADE'), nullable=False)

    customer = relationship("UserProfileModel", back_populates="tasks")
    responses = relationship("TaskResponseModel", back_populates="task", cascade="all, delete-orphan",
                             uselist=False)
    reviews = relationship("ReviewModel", back_populates="task", cascade="all, delete-orphan")
