from sqlalchemy import Column, Integer, Enum, Numeric
from sqlalchemy.orm import relationship

from src.database.base import Base


class SubscriptionPlanModel(Base):
    __tablename__ = 'subscriptions_plan'

    id = Column(Integer, primary_key=True)
    period = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)

    subscriptions = relationship('SubscriptionModel', back_populates='plan')