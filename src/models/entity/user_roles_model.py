from sqlalchemy import Column, Integer, ForeignKey

from src.database.base import Base


class UserRolesModel(Base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)

