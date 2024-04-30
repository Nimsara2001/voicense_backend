from fastapi import APIRouter
from note_generator.transcription_generator import get_transcription

router = APIRouter(
    prefix="/record",
)


@router.get("/upload")
async def upload_record():
    return {get_transcription()}
