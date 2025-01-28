from sqlalchemy import Column, Integer, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime

class ReviewModel(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('user_profile.id', ondelete='CASCADE'), nullable=False)
    executor_id = Column(Integer, ForeignKey('user_profile.id', ondelete='CASCADE'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    rating = Column(Boolean, nullable=False)  # True для "плюс", False для "минус"
    comment = Column(Text, nullable=True)  # Текст отзыва
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    customer = relationship("UserProfileModel", foreign_keys=[customer_id], back_populates="reviews_left")
    executor = relationship("UserProfileModel", foreign_keys=[executor_id], back_populates="reviews_received")
    task = relationship("TasksModel", back_populates="reviews")
