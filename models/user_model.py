from typing import Optional
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: str = Field(...)
    user_type: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "vcs0001",
                "user_type": "admin",
                "first_name": "John",
                "last_name": "Doe",
                "username": "mihin",
                "password": "1234",
            }
        }


class UpdateUserModel(BaseModel):
    user_id: Optional[str]
    user_type: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "user_id": "vcs0001",
                "user_type": "admin",
                "first_name": "John",
                "last_name": "Doe",
                "username": "mihin",
                "password": "1234",
            }
        }


# def ResponseModel(data, message):
#     return {
#         "data": [data],
#         "code": 200,
#         "message": message,
#     }
#
#
# def ErrorResponseModel(error, code, message):
#     return {"error": error, "code": code, "message": message}
