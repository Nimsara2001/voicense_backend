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
    try:
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
            else:
                db_save = await save_note_and_transcription(note, transcription["result"], module_id)
                if db_save["message"] == "failed":
                    return db_save

                file_delete = await controller.delete_audio(res["path"])

        return {
            "message": "success",
            "user_id": user_id,
            "note_id": db_save["note_id"],
            "module_id": db_save["module_id"],
            "file_delete": file_delete["message"]
        }
    except Exception as e:
        return {"message": "failed", "detail": str(e)}
