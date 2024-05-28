from typing import Optional

from pydantic import BaseModel, Field


class Module(BaseModel):
    title: str = Field(...)
    created_date: str = Field(...)
    last_accessed: str = Field(...)
    is_deleted: bool = Field(default=False)
    notes: Optional[list] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python Core",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01 20:47:06.932514",
                "is_deleted": False,
                "notes": []
            }
        }


def get_module_schema(module):
    return {
        "_id": str(module["_id"]),
        "title": module["title"],
        "created_date": module["created_date"],
        "last_accessed": module["last_accessed"],
        "is_deleted": module["is_deleted"],
        "notes": [str(note_id) for note_id in module["notes"]]
    }
