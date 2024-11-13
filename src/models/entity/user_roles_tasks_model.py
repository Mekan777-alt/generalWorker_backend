from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class UserRolesTasksModel(Base):
    __tablename__ = 'user_roles_tasks'

    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    done_create_task = Column(Integer, nullable=False)

    roles_tasks = relationship('RoleModel', back_populates='done_create_task')