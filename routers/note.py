from bson import ObjectId
from fastapi import APIRouter

from db_config import get_db

router = APIRouter(
    prefix="/note",
)


@router.get("/recent")
async def recent_notes():
    # overrite on the markdown_view file
    db = get_db()
    note = db["testnote"].find_one({"_id":ObjectId('6632988b3cb9a65b5fb9af39')})
    user = db["User"].find_one({"_id":"VCSL0010"})
    print(user)
    with open('resources/markdown_view.md', 'w',encoding='utf-8') as f:
        f.write(note["note"])
    return {note["note"]}


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
