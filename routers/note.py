from fastapi import APIRouter
import controller.note_controller as controller

router = APIRouter(
    prefix="/note"
)


@router.get("/recent")
async def recent_notes():
    try:
        notes = await controller.recently_accessed_notes()
        return notes
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.get("/{note_id}")
async def view_note(note_id: str):
    try:
        note = await controller.get_note_by_id(note_id)
        return note
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.put("/update_accessed/{note_id}")
async def update_accessed(note_id: str):
    try:
        response = await controller.update_last_accessed(note_id)
        return response
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.put("/trash/{note_id}")
async def trash_note(note_id: str):
    try:
        response = await controller.trash_note_by_id(note_id)
        return response
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.post("/restore/{note_id}")
async def restore_trash_note(note_id: str):
    try:
        response = await controller.restore_note_by_id(note_id)
        return response
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.delete("/delete/{note_id}")
async def delete_note(note_id: str):
    try:
        response = await controller.delete_note_by_id_permanently(note_id)
        return response
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.post("/search")
async def search_notes(search_query: str):
    try:
        notes = await controller.search_notes_by_prompt(search_query)
        return notes
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.post("/share/{note_id}")
async def share_note(note_id: str):
    return {"message": "Note shared"}
