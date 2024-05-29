from fastapi import APIRouter
from note_generator.optimizer import optimize_note
from controller.note_controller import (delete_note_by_id_permanently, 
                                        get_note_by_id, 
                                        recently_accessed_notes, 
                                        restore_note_by_id, 
                                        trash_note_by_id)


router = APIRouter(
    prefix="/note"
)


@router.get("/recent")
async def recent_notes():
    with open('resources/transcription.txt', 'r') as file:
        transcription = file.read()
    note = optimize_note(transcription)
    with open('resources/markdown_view.md', 'w') as file:
        file.write(note)
    return {"note": note}


#this gives the recent notes we have accessed
@router.get("/recentnotes")
async def recent_notes():
    notes= await recently_accessed_notes()
    return notes
    # return {"message": "Recent notes"}

#todo: search notes
@router.post("/search")
async def search_notes():
    return {"message": "Search notes"}


@router.get("/{note_id}")
async def view_note(note_id: str):
    note = await get_note_by_id(note_id)
    return note

@router.put("/trash/{note_id}")
async def trash_note(note_id: str):
    response = await trash_note_by_id(note_id)
    return response

@router.put("/restore/{note_id}")
async def restore_trash_note(note_id: str):
    response = await restore_note_by_id(note_id)
    return response

@router.delete("/delete/{note_id}")
async def delete_note(note_id: str):
    response = await delete_note_by_id_permanently(note_id)
    return response

#todo: share note
@router.post("/share/{note_id}")
async def share_note(note_id: int):
    return {"message": "Note shared"}
