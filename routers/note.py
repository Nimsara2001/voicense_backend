from fastapi import APIRouter
from note_generator.optimizer import optimize_note

router = APIRouter(
    prefix="/note",
)


@router.get("/recent")
async def recent_notes():
    with open('resources/transcription.txt', 'r') as file:
        transcription = file.read()
    note = optimize_note(transcription)
    with open('resources/markdown_view.md', 'w') as file:
        file.write(note)
    return {"note": note}


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
