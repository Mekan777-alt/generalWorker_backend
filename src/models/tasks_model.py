from sqlalchemy import Column, String, Integer, NUMERIC
from src.database.base import Base

class TasksModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(NUMERIC, nullable=False)

