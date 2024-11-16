from enum import Enum

class TaskResponseStatusEnum(str, Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
