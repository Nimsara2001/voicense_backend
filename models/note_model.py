from typing import Optional
from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    note_id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    content: str = Field(...)
    created_date: str
    last_accessed: str
    transcription_id: str = Field(...)
    module_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "note_id": "n0001",
                "title": "Python",
                "description": "Python Programming",
                "content": "Python is a programming language that lets you work quickly and integrate systems more effectively.",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01",
                "transcription_id": "t0001",
                "module_id": "m0001",
            }
        }

class UpdateNoteModel(BaseModel):
    note_id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    content: Optional[str]
    created_date: Optional[str]
    last_accessed: Optional[str]
    transcription_id: Optional[str]
    module_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "note_id": "n0001",
                "title": "Python",
                "description": "Python Programming",
                "content": "Python is a programming language that lets you work quickly and integrate systems more effectively.",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01",
                "transcription_id": "t0001",
                "module_id": "m0001",
            }
        }