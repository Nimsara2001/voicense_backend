from fastapi import APIRouter
import controller.note_controller as controller
from fastapi.responses import FileResponse
router = APIRouter(
    prefix="/note"
)


@router.get("/recent")
async def recent_notes(user_id: str):
    # print("accesssesdd")
    notes = await controller.recently_accessed_notes(user_id)
    # print(notes)
    return notes


@router.get("/{note_id}")
async def view_note(note_id: str):
    note = await controller.get_note_by_id(note_id)
    return note


@router.get("/trashed")
async def get_all_trashed_notes(user_id: str):
    print("trashed notes accessed")
    notes = await controller.get_all_trashed_notes(user_id)
    return notes


@router.post("/update_accessed/{note_id}")
async def update_accessed(note_id: str):
    response = await controller.update_last_accessed(note_id)
    return response


@router.patch("/trash/{note_id}")
async def trash_note(note_id: str):
    print("trashed note", note_id)
    response = await controller.trash_and_restore_note_by_id(note_id, True)
    return response


@router.patch("/restore/{note_id}")
async def restore_trash_note(note_id: str):
    response = await controller.trash_and_restore_note_by_id(note_id, False)
    return response


@router.post("/delete")
async def delete_note(module_id: str, note_id: str):
    response = await controller.delete_note_by_id_permanently(module_id, note_id)
    return response


@router.post("/search")  # try to implement in frontend
async def search_notes(search_query: str):
    notes = await controller.search_notes_by_prompt(search_query)
    return notes


@router.post("/share/{note_id}")  # implement later
async def share_note(note_id: str):
    print("note shared", note_id)
    return {"message": "Note shared"}


@router.get("/download/{note_id}")
async def download_note(note_id: str):
    response = await controller.download_note_by_id(note_id)
    file_path = response["path"]  # Assuming this is the path to the PDF file
    return FileResponse(path=file_path, media_type='application/pdf', filename=file_path.split("/")[-1])

@router.put("/insert_recent")
async def insert_to_recent(userId:str,noteId:str):
    response = await controller.insert_to_recentNoteList(userId,noteId)
    return response
