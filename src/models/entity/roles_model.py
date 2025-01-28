from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class RoleModel(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # user_roles = relationship('UserRolesModel', back_populates='role_roles')
    # users = relationship("UserProfileModel", secondary="user_roles", back_populates="roles")
    user_roles = relationship('UserRolesModel', back_populates="role")