from sqlalchemy import Column, Integer, Enum, Numeric

from models.enums.subscription_period_enum import SubscriptionPeriodEnum
from src.database.base import Base
from enum import Enum as PyEnum


class SubscriptionModel(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    period = Column(Enum(SubscriptionPeriodEnum), nullable=False)
    price = Column(Numeric, nullable=False)
