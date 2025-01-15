from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from src.database.base import Base


class SubscriptionModel(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_profile.id', ondelete='CASCADE'), nullable=False)
    plan_id = Column(Integer, ForeignKey('subscriptions_plan.id', ondelete='CASCADE'), nullable=False)
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship('UserProfileModel', back_populates='subscriptions')
    plan = relationship('SubscriptionPlanModel', back_populates='subscriptions')