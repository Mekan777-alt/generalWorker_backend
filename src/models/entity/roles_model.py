from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.base import Base


class RoleModel(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    rating = relationship("UserRoleRatingModel", back_populates="roles")
    user_roles = relationship('UserRolesModel', back_populates='role_roles')