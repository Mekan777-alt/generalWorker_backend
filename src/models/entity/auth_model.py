from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.base import Base


class AuthModel(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phoneNumber = Column(String, nullable=False)
    otpCode = Column(String(6), nullable=True, comment="Код одноразового пароля для подтверждения авторизации")
    otpExpiry = Column(DateTime, nullable=True, comment="Время истечения срока действия OTP")
    createdAt = Column(DateTime, server_default=func.now(), nullable=False, comment="Дата создания записи")
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False,
                        comment="Дата последнего обновления записи")
    isActive = Column(Boolean, default=False)

    user_profile = relationship("UserProfileModel", back_populates="auth", uselist=False, cascade="all, delete-orphan")
    # user_roles = relationship('UserRolesModel', back_populates='auth', cascade="all, delete-orphan")