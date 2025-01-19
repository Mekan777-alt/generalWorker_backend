from enum import Enum as PyEnum

class ResponseStatus(PyEnum):
    REJECTED = 'Отклонен'
    ACCEPTED = 'Принял'
    EXPECTATION = 'Ожидание'