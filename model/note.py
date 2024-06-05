from pydantic import BaseModel, Field


class Note(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    content: str = Field(...)
    created_date: str = Field(...)
    last_accessed: str = Field(...)
    is_deleted: bool = Field(default=False)


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
