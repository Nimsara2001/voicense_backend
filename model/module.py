from typing import Optional

from pydantic import BaseModel, Field


class Module(BaseModel):
    title: str = Field(...)
    created_date: str = Field(...)
    last_accessed: str = Field(...)
    notes: Optional[list] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python Core",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01",
                "notes": ["VCSN0001", "VCSN0002", "VCSN0003"]
            }
        }
