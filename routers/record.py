from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Body, BackgroundTasks
import controller.transcription_controller as controller
from note_generator.optimizer import optimize_note

router = APIRouter(
    prefix="/record"
)


@router.post("/upload")
async def upload_record(
        file: Annotated[UploadFile, File],
        user_id: Annotated[str, Body],
        module_id: Annotated[str, Body],
        background_tasks: BackgroundTasks
):
    # res = await controller.save_audio(file)
    #
    # if res["message"] == "failed":
    #     return res
    # else:
    #     transcription = await controller.generate_transcription(res["path"])
    #     note = optimize_note(transcription)
    #
    #
    # return {
    #     "path": res["path"], "message": "successful",
    #     "details": {
    #         "user_id": user_id,
    #         "module_id": module_id
    #     },
    #     "transcription": transcription,
    #     "note":note
    # }
    res = await controller.save_audio(file)
    print(res["path"])
    background_tasks.add_task(process_after_upload, res["path"], user_id, module_id)

    return {"message": "File uploaded successfully."}


async def process_after_upload(path, user_id, module_id):
    transcription = await controller.generate_transcription(path)
    print(transcription)

    note = optimize_note(transcription)
    print(note)
