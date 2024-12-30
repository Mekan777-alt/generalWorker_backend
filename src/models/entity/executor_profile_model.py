from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.database.base import Base

class ExecutorProfileModel(Base):
    __tablename__ = 'executor_profile'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    location = Column(String, nullable=True)
    aboutMySelf = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    auth_id = Column(Integer, ForeignKey('auth.id', ondelete='CASCADE'), nullable=True)

    auth_info = relationship("AuthModel", back_populates="executor")
    responses = relationship("TaskResponseModel", back_populates="executor", cascade="all, delete-orphan")
    reviews_received = relationship("ReviewModel", back_populates="executor")  # Отзывы, полученные исполнителем
