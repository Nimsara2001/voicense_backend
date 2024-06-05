from bson.errors import InvalidId

from db_config import get_db
from fastapi import HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from model.module import get_module_schema
from model.note import get_note_schema

modules_collection = None
notes_collection = None
users_collection = None

async def get_collection():
    global modules_collection, notes_collection, users_collection

    db = await get_db()
    if db is None:
        raise Exception("Failed to get database connection")

    if modules_collection is None:
        modules_collection = db["Module"]

    if notes_collection is None:
        notes_collection = db["Note"]

    if users_collection is None:
        users_collection = db["User"]


async def get_all_modules_func(user_id: str):
    await get_collection()
    try:
        user_id = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    user = await users_collection.find_one({"_id": user_id})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    modules = []
    for module_id in user["modules"]:
        module = await modules_collection.find_one({"_id": module_id})
        if module is not None:
            modules.append(module)

    if len(modules) == 0:
        raise HTTPException(status_code=404, detail=f"No modules found for the specified {user_id}")
    else:
        module_schemas = [get_module_schema(module) for module in modules]

    return module_schemas


async def get_all_notes_of_module_func(module_id: str,is_other:bool):
    await get_collection()
    try:
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid module_id")

    module = await modules_collection.find_one({"_id": module_id})

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    if is_other:
        if not module["title"].endswith("_other"):
            raise HTTPException(status_code=400, detail="Module is not an other module")
    else:
        if module["title"].endswith("_other"):
            raise HTTPException(status_code=400, detail="Module is an other module")

    notes = []
    for note_id in module["notes"]:
        note = await notes_collection.find_one({"_id": note_id})
        if note is not None:
            notes.append(note)

    if len(notes) == 0:
        raise HTTPException(status_code=404, detail="No notes found for the specified module_id")
    else:
        note_schema = [get_note_schema(note) for note in notes]

    return note_schema


async def search_module_func(search_text: str):
    await get_collection()

    await modules_collection.create_index([("title", "text")])

    module_cursor = modules_collection.find({
        "$text": {"$search": search_text},
        "title": {"$not": {"$regex": "_other$"}}
    })

    modules = await module_cursor.to_list(length=100)

    if modules:
        search_modules = [get_module_schema(module) for module in modules]
        return search_modules
    else:
        return {"message": "failed", "detail": "No module found"}


async def trash_module_func(module_id: str):
    await get_collection()
    try:
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid module_id")

    module = await modules_collection.find_one({"_id": module_id})

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    if module["title"].endswith("_other"):
        raise HTTPException(status_code=400, detail="Cannot trash other module")

    updated_result = await modules_collection.update_one(
        {"_id": module_id},
        {"$set": {"is_deleted": True}}
    )

    if updated_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to trash module")

    return {"message": "success", "detail": "Module trashed successfully"}
