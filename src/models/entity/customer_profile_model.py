from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.database.base import Base

class CustomerProfileModel(Base):
    __tablename__ = 'customer_profile'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    location = Column(String, nullable=True)
    aboutMySelf = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    auth_id = Column(Integer, ForeignKey('auth.id'), nullable=True)

    auth_info = relationship("AuthModel", back_populates="customer")
    tasks = relationship("TasksModel", back_populates="customer")
    reviews_left = relationship("ReviewModel", back_populates="customer")  # Отзывы, оставленные заказчиком

