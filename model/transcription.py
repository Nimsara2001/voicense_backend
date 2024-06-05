from bson import ObjectId
from pydantic import BaseModel, Field


class Transcription(BaseModel):
    content: str = Field(...)
    generated_date: str = Field(...)
    note_id: ObjectId = Field(...)

    class Config:
        arbitrary_types_allowed = True


def get_transcription_schema(transcription):
    return {
        "id": str(transcription["_id"]),
        "content": transcription["content"],
        "generated_date": transcription["generated_date"],
        "note_id": str(transcription["note_id"]) if transcription["note_id"] else ""
    }
