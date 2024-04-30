from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# transcription
#    -transcriptionId
#    -content
#    -generatedDate

class UserSchema(BaseModel):
    transcription_id: str = Field(...)
    content: str = Field(...)
    generatedDate: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "transcription_id": "TRC0001",
                "content": "this is a sample transcription content",
                "generatedDate": "2024-05-21"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
