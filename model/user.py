from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class UserType(str, Enum):
    Student = "Student"
    Lecturer = "Lecturer"


class User(BaseModel):
    user_type: UserType = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    modules: Optional[list] = Field(default=[])

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "user_type": "Student",
                "first_name": "Mihin",
                "last_name": "Premarathna",
                "username": "mihin",
                "password": "mihin123",
                "modules": []
            }
        }


class LoginUser(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "mihin",
                "password": "mihin123"
            }
        }


def get_user_schema(user):
    return {
        "id": str(user["_id"]),
        "user_type": user["user_type"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "hashed_password": str(user["password"])
    }
