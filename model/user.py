from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: str = Field(...)
    user_type: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    modules: Optional[list] = []

    class Config:
        schema_extra = {
            "example": {
                "user_id": "VCSS0001",
                "user_type": "Student",
                "first_name": "Mihin",
                "last_name": "Premarathna",
                "username": "mihin",
                "password": "mihin123",
                "modules": ["VCSM0001", "VCSM0002", "VCSM0003"]
            }
        }
