from sqlalchemy.orm import relationship

from src.database.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey


class QuestionRequestModel(Base):
    __tablename__ = 'question_request'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)

    photo = relationship('QuestionRequestPhotoModel', back_populates='question')
    user = relationship('UserProfileModel', back_populates='questions')
