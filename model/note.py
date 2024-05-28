from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class Note(BaseModel):
    title: str = Field(...)
    description: str = Field(...)  # show in the note view card
    content: str = Field(...)
    created_date: str
    last_accessed: str
    is_deleted: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "60d5ec88b35866cc8fe16e6e",
                "title": "Python Programming",
                "description": "Python is a programming language that lets you work quickly and integrate systems "
                               "more effectively.",
                "content": "Python is a programming language that lets you work quickly and integrate systems more "
                           "effectively. It is a powerful language that is easy to learn and easy to read. Python is a",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01 20:47:06.932514",

            }
        }


def get_note_schema(note):
    return {
        "_id": str(note["_id"]),
        "title": note["title"],
        "description": note["description"],
        "content": note["content"],
        "created_date": note["created_date"],
        "last_accessed": note["last_accessed"],
        "is_deleted": note["is_deleted"]
    }
