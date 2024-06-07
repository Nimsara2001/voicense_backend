from fastapi import APIRouter
import controller.note_controller as controller

router = APIRouter(
    prefix="/note"
)


@router.get("/recent")
async def recent_notes(user_id: str):
    notes = await controller.recently_accessed_notes(user_id)
    return notes


@router.get("/{note_id}")
async def view_note(note_id: str):
    note = await controller.get_note_by_id(note_id)
    return note


@router.post("/update_accessed/{note_id}")
async def update_accessed(note_id: str):
    response = await controller.update_last_accessed(note_id)
    return response


@router.post("/trash/{note_id}")
async def trash_note(note_id: str):
    response = await controller.trash_and_restore_note_by_id(note_id, True)
    return response


@router.post("/restore/{note_id}")
async def restore_trash_note(note_id: str):
    response = await controller.trash_and_restore_note_by_id(note_id, False)
    return response


@router.post("/delete")
async def delete_note(module_id: str, note_id: str):
    response = await controller.delete_note_by_id_permanently(module_id, note_id)
    return response


@router.post("/search") # try to implement in frontend
async def search_notes(search_query: str):
    notes = await controller.search_notes_by_prompt(search_query)
    return notes


@router.post("/share/{note_id}")  # implement later
async def share_note(note_id: str):
    return {"message": "Note shared"}
