from sqlalchemy import Column, String, Integer
from database.base import Base
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


class AdminModel(Base):
    __tablename__ = 'auth_admin'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password_hash = Column(String)

    def set_password(self, plain_password):
        self.password_hash = ph.hash(plain_password)

    # Метод для проверки пароля
    def verify_password(self, plain_password):
        try:
            return ph.verify(self.password_hash, plain_password)
        except VerifyMismatchError:
            return False
