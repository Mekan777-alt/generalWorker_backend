from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from database.base import Base


class UserRolesModel(Base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('user_profile.id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    is_use = Column(Boolean, default=False)
    token = Column(String, nullable=True)

    user = relationship('UserProfileModel', back_populates="user_roles")
    role = relationship('RoleModel', back_populates="user_roles")