from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.database.base import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    phoneNumber = Column(String, nullable=False)
    location = Column(String, nullable=True)
    aboutMySelf = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    verifyCode = Column(String, nullable=True)

    codeCreatedAt = Column(DateTime, default=datetime.utcnow)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)
    isActive = Column(Boolean, nullable=False, default=True)
    isRegistered = Column(Boolean, nullable=False, default=False)


    roles = relationship("Role", secondary="user_roles", back_populates="users")