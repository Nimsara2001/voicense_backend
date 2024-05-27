from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Transcription(BaseModel):
    content: str = Field(...)
    generated_date: str = Field(...)
    note_id: Optional[str] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "content": "Hello, my name is Chandu Nair and I am going to be handling the subject of marketing",
                "generated_date": "2024-05-21",
                "note_id": None
            }
        }


def get_transcription_schema(transcription):
    return {
        "id": str(transcription["_id"]),
        "content": transcription["content"],
        "generated_date": transcription["generated_date"],
        "note_id": str(transcription["note_id"]) if transcription["note_id"] else ""
    }
