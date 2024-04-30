from typing import Optional
from pydantic import BaseModel, Field


class ModuleSchema(BaseModel):
    module_id: str = Field(...)
    title: str = Field(...)
    created_date: str = Field(...)
    last_accessed: str = Field(...)
    user_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "module_id": "m0001",
                "title": "Python Core",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01",
                "user_id": "u0001",
            }
        }


class UpdateNoteModel(BaseModel):
    module_id: Optional[str]
    title: Optional[str]
    created_date: Optional[str]
    last_accessed: Optional[str]
    user_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "module_id": "m0001",
                "title": "Python Core",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01",
                "user_id": "u0001",
            }
        }
