from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Body
import controller.transcription_controller as controller
from controller.note_controller import save_note_and_transcription
from note_generator.optimizer import optimize_note

router = APIRouter(
    prefix="/record"
)


@router.post("/upload")
async def upload_record(
        file: Annotated[UploadFile, File],
        user_id: Annotated[str, Body],
        module_id: Annotated[str, Body],
):
    res = await controller.save_audio(file)

    if res["message"] == "failed":
        return res
    else:
        transcription = await controller.generate_transcription(res["path"])
        if transcription["message"] == "failed":
            return transcription

        note = optimize_note(transcription["result"])
        if note["message"] == "failed":
            return note

        await save_note_and_transcription(note, transcription["result"], module_id)

        await controller.delete_audio(res["path"])

    return {
        "message": "successful",
        "user_id": user_id,
        "transcription": transcription,
        "note": note
    }


@router.get("/test")
async def test():
    note = {"title": "test", "content": "test"}
    transcription = "test"
    module_id = "6638b74cf81ffd971fadfa68"

    res=await save_note_and_transcription(note, transcription, module_id)

    return res
