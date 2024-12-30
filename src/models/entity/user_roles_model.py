from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.database.base import Base


class UserRolesModel(Base):
    __tablename__ = 'user_roles'

    auth_id = Column(Integer, ForeignKey('auth.id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    is_use = Column(Boolean, default=False)

    auth_roles = relationship('AuthModel', back_populates='user_roles')
    role_roles = relationship('RoleModel', back_populates='user_roles')