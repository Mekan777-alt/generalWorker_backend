from enum import Enum as PyEnum

class TasksStatusEnum(PyEnum):
    SEARCH = 'SEARCH'
    WORK = 'WORK'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    UNDER_REVIEW = 'UNDER_REVIEW'
