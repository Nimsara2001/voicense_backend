from datetime import datetime
import re

from db_config import get_db
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

from model.note import Note, get_note_schema
from model.transcription import Transcription

notes_collection = None
transcriptions_collection = None
modules_collection = None


async def get_collection():
    global notes_collection, transcriptions_collection, modules_collection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")

    if notes_collection is None:
        notes_collection = db["Note"]

    if transcriptions_collection is None:
        transcriptions_collection = db["Transcription"]

    if modules_collection is None:
        modules_collection = db["Module"]


async def recently_accessed_notes():
    await get_collection()

    notes_cursor = notes_collection.find({"is_deleted": False}).sort([("last_accessed", -1)]).limit(10)
    notes = await notes_cursor.to_list(length=100)

    recent_notes = [get_note_schema(note) for note in notes]

    return recent_notes


async def get_note_by_id(note_id: str):
    await get_collection()
    try:
        note_id = ObjectId(note_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id")

    try:
        note = await notes_collection.find_one({"_id": note_id, "is_deleted": False})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if note:
        return get_note_schema(note)
    else:
        raise HTTPException(status_code=404, detail="Note not found")


async def update_last_accessed(note_id: str):
    await get_collection()
    try:
        note_id = ObjectId(note_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id")

    updated_result = await notes_collection.update_one(
        {"_id": note_id, "is_deleted": False},
        {"$set": {"last_accessed": str(datetime.now())}}
    )

    if updated_result.modified_count == 1:
        return {"message": "success", "detail": f"Note with ID {note_id} last accessed updated"}
    else:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


async def trash_note_by_id(note_id: str):
    await get_collection()
    try:
        note_id = ObjectId(note_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id")

    updated_result = await notes_collection.update_one({"_id": note_id}, {"$set": {"is_deleted": True}})

    if updated_result.modified_count == 1:
        return {"message": "success", "detail": f"Note with ID {note_id} has been trashed"}
    else:
        raise HTTPException(status_code=404, detail=f"Item with ID {note_id} not found or already trashed")


async def restore_note_by_id(note_id: str):
    await get_collection()
    try:
        note_id = ObjectId(note_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id")

    updated_result = await notes_collection.update_one({"_id": note_id}, {"$set": {"is_deleted": False}})

    if updated_result.modified_count == 1:
        return {"message": "success", "detail": f"Note with ID {note_id} has been restored"}
    else:
        raise HTTPException(status_code=404, detail=f"Item with ID {note_id} not found or already restored")


async def delete_note_by_id_permanently(note_id: str):
    await get_collection()
    try:
        note_id = ObjectId(note_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id")

    result = await notes_collection.delete_one({"_id": note_id, "is_deleted": True})

    if result.deleted_count == 1:
        return {"message": "success", "detail": f"Note with ID {note_id} has been deleted permanently"}
    elif result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found or already deleted")
    else:
        raise HTTPException(status_code=400, detail=f"Unexpected error occurred while deleting note with ID {note_id}")


async def save_note_and_transcription(note, transcription, module_id):
    await get_collection()

    new_note = Note(
        title=note["title"],
        description=extract_description(note["content"]),
        content=note["content"],
        created_date=str(datetime.now()),
        last_accessed=str(datetime.now()),
    )

    note_result = await notes_collection.insert_one(new_note.dict())
    if note_result.inserted_id is None:
        return {"message": "failed", "detail": "Note insertion failed"}

    new_transcription = Transcription(
        content=transcription,
        generated_date=str(datetime.now()),
        note_id=ObjectId(note_result.inserted_id),
    )

    transcription_result = await transcriptions_collection.insert_one(new_transcription.dict())
    if transcription_result.inserted_id is None:
        return {"message": "failed", "detail": "Transcription insertion failed"}

    add_module_res = await add_note_to_module(note_result.inserted_id, module_id)
    if add_module_res["message"] == "failed":
        return add_module_res

    return {"message": "success", "note_id": str(note_result.inserted_id), "module_id": module_id}


def extract_description(note):
    no_markdown = re.sub(r'[*_#\n]', '', note)
    description = no_markdown[:220]

    return description


async def add_note_to_module(note_id, module_id):
    await get_collection()

    try:
        note_id = ObjectId(note_id)
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id or module_id")

    module = await modules_collection.find_one({"_id": module_id})

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    updated_result = await modules_collection.update_one(
        {"_id": module_id},
        {"$push": {"notes": note_id}}
    )

    if updated_result.modified_count == 0:
        return {"message": "failed", "detail": "Failed to add note to module"}

    return {"message": "success", "detail": "Note added to module successfully"}


async def search_notes_by_prompt(search_query: str):
    await get_collection()

    await notes_collection.create_index([("title", "text"), ("description", "text")])

    notes_cursor = notes_collection.find({"$text": {"$search": search_query}})

    notes = await notes_cursor.to_list(length=100)

    if notes:
        search_notes = [get_note_schema(note) for note in notes]
        return search_notes
    else:
        raise HTTPException(status_code=404, detail="No notes found")

# def get_content_as_md(content: str):
#     os.makedirs("resources/markdown", exist_ok=True)
#     file_name = token_hex(10)
#
#     file_path = f"resources/markdown/{file_name}.md"
#
#     with open(file_path, 'w') as f:
#         f.write(content)
#
#     return file_path
