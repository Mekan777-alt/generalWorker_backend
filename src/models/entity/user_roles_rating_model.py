from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class UserRoleRatingModel(Base):
    __tablename__ = 'user_roles_rating'

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    plus = Column(Integer, default=0)
    minus = Column(Integer, default=0)


    roles = relationship("RoleModel", back_populates="rating")
