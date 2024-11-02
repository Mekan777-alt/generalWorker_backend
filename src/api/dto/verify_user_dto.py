from pydantic import BaseModel, Field


class VerifySMSRequest(BaseModel):
    id_token: str = Field(..., description='The id_token from firebase')


class VerifySMSResponse(BaseModel):
    id: int = Field(..., description='ID')
    firebase_uid: str = Field(..., description='Firebase UID')
    firstName: str = Field(..., description='First Name')
    lastName: str = Field(..., description='Last Name')
    photo: str = Field(..., description='Photo')
