from enum import Enum as PyEnum

class TasksStatusEnum(PyEnum):
    CREATED = 'CREATED'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
