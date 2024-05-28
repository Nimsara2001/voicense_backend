from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Body
import controller.transcription_controller as controller

router = APIRouter(
    prefix="/record",
)


@router.post("/upload")
async def upload_record(file: Annotated[UploadFile, File],
                        user_id: Annotated[str, Body],
                        module_id: Annotated[str, Body]):
    res = await controller.save_audio(file)

    if res["message"] == "failed":
        return res
    else:
        transcription = await controller.generate_transcription(res["path"])

    return {"path": res["path"], "message": "successful",
            "details":
                {"user_id": user_id,
                 "module_id": module_id},
            "transcription": transcription,
            }
