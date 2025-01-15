from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database.base import Base


class UserProfileModel(Base):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    about_myself = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    auth_id = Column(Integer, ForeignKey('auth.id', ondelete='CASCADE'), nullable=False, unique=True)

    auth = relationship("AuthModel", back_populates="user_profile")
    roles = relationship("RoleModel", secondary="user_roles", back_populates="users")

    tasks = relationship("TasksModel", back_populates="customer")
    responses = relationship("TaskResponseModel", back_populates="executor", cascade="all, delete-orphan")
    reviews_left = relationship("ReviewModel", foreign_keys="ReviewModel.customer_id", back_populates="customer")
    reviews_received = relationship("ReviewModel", foreign_keys="ReviewModel.executor_id", back_populates="executor")
    subscriptions = relationship('SubscriptionModel', back_populates='user')
