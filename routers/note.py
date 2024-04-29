from fastapi import APIRouter

router = APIRouter(
    prefix="/note",
)


@router.get("/recent")
async def recent_notes():
    return {"message": "Recent notes"}


@router.post("/search")
async def search_notes():
    return {"message": "Search notes"}


@router.get("/{note_id}")
async def view_note(note_id: int):
    return {"message": "view note content"}


@router.delete("/trash/{note_id}")
async def trash_note(note_id: int):
    return {"message": "Note trashed"}


@router.post("/share/{note_id}")
async def share_note(note_id: int):
    return {"message": "Note shared"}