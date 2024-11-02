import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    photo = Column(String, nullable=True)

    roles = relationship("Role", secondary="user_roles", back_populates="users")