from sqlalchemy.orm import relationship

from database.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey

class QuestionRequestPhotoModel(Base):
    __tablename__ = 'question_request_photo_model'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question_request.id'))
    photo_url = Column(String, nullable=True)

    question = relationship('QuestionRequestModel', back_populates='photo')