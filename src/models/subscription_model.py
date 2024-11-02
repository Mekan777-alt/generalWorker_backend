from sqlalchemy import Column, Integer, Enum, Numeric
from src.database.base import Base
from enum import Enum as PyEnum

class SubscriptionPeriod(PyEnum):
    ONE_MONTH = 1
    THREE_MONTHS = 3
    TWELVE_MONTHS = 12


class SubscriptionModel(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    period = Column(Enum(SubscriptionPeriod), nullable=False)
    price = Column(Numeric, nullable=False)

