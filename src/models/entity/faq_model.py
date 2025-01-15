from src.database.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class FAQModel(Base):
    __tablename__ = 'faq'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)