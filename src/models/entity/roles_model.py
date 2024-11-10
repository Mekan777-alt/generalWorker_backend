from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.base import Base


class RoleModel(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("UsersModel", secondary="user_roles", back_populates="roles")