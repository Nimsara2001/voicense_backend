import re
from datetime import datetime
from bson.errors import InvalidId
from pymongo import errors

from db_config import get_db, client
from fastapi import HTTPException
from bson import ObjectId

from model.module import get_module_schema, Module
from model.note import get_note_schema

modules_collection = None
notes_collection = None
users_collection = None


async def get_collection():
    global modules_collection, notes_collection, users_collection

    db = await get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

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
        module = await modules_collection.find_one({"_id": module_id, "is_deleted": False})
        if module is not None:
            modules.append(module)

    if len(modules) == 0:
        raise HTTPException(status_code=404, detail=f"No modules found for the specified {user_id}")
    else:
        module_schemas = [get_module_schema(module) for module in modules]

    return module_schemas


async def get_all_notes_of_module_func(module_id: str):
    await get_collection()
    try:
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid module_id")

    module = await modules_collection.find_one({"_id": module_id})

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    notes = []
    for note_id in module["notes"]:
        note = await notes_collection.find_one({"_id": note_id, "is_deleted": False})
        if note is not None:
            notes.append(note)

    if len(notes) == 0:
        raise HTTPException(status_code=404, detail="No notes found for the specified module_id")
    else:
        note_schema = [get_note_schema(note) for note in notes]

        result = await update_last_accessed(module_id)
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update last accessed time")

    return note_schema


async def update_last_accessed(module_id: ObjectId):
    result = await modules_collection.update_one(
        {"_id": module_id},
        {"$set": {"last_accessed": str(datetime.now())}}
    )

    return result


async def get_user_modules(user_id: str):
    await get_collection()

    try:
        user_id = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    user = await users_collection.find_one({"_id": user_id})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_modules = []
    for module_id in user["modules"]:
        module = await modules_collection.find_one({"_id": module_id, "is_deleted": False})
        if module is not None:
            user_modules.append(module)

    if len(user_modules) == 0:
        raise HTTPException(status_code=404, detail=f"No modules found for the specified {user_id}")

    return user_modules


async def search_module_func(user_id: str, search_text: str):
    await get_collection()

    if not re.match('^[a-zA-Z0-9 ]*$', search_text):
        raise HTTPException(status_code=400, detail="Module title contains invalid characters")

    user_modules = await get_user_modules(user_id)

    await modules_collection.create_index([("title", "text")])

    search_modules = []
    for module in user_modules:
        if search_text.lower() in module["title"].lower():
            search_modules.append(get_module_schema(module))

    if search_modules:
        return search_modules
    else:
        raise HTTPException(status_code=404, detail="No modules found for the specified search_text")


async def trash_and_restore_module_func(module_id, is_trash: bool):
    await get_collection()
    try:
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid module_id")

    module = await modules_collection.find_one({"_id": module_id})

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    if module["title"].endswith("_other"):
        raise HTTPException(status_code=400, detail="Cannot trash or restore other module")

    async with await client.start_session() as s:
        async with s.start_transaction():
            try:
                updated_result = await modules_collection.update_one(
                    {"_id": module_id},
                    {"$set": {"is_deleted": is_trash}},
                    session=s
                )

                if updated_result.modified_count == 0:
                    raise HTTPException(status_code=500, detail="Failed to trash or restore module")

                for note_id in module["notes"]:
                    if note_id is None:
                        continue
                    updated_result = await notes_collection.update_one(
                        {"_id": note_id},
                        {"$set": {"is_deleted": is_trash}},
                        session=s
                    )

                    if updated_result.modified_count == 0:
                        raise HTTPException(status_code=500, detail="Failed to trash or restore note")

                s.commit_transaction()

                action = "trashed" if is_trash else "restored"
                return {"message": "success", "detail": f"Module {action} successfully"}

            except Exception as e:
                s.abort_transaction()
                raise HTTPException(status_code=500, detail=str(e))


async def add_module_func(title: str, user_id: str):
    await get_collection()

    if not re.match('^[a-zA-Z0-9 ]*$', title):
        raise HTTPException(status_code=400, detail="Module title contains invalid characters")

    module = Module(
        title=title,
        created_date=str(datetime.now()),
        last_accessed=str(datetime.now())
    )

    module_id = await modules_collection.insert_one(module.dict())

    if module_id is None:
        raise HTTPException(status_code=500, detail="Failed to add module")

    await add_module_into_user(user_id, module_id.inserted_id)

    return await get_module_by_id(str(module_id.inserted_id))


async def add_module_into_user(user_id: str, module_id: ObjectId):
    await get_collection()

    try:
        user_id = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    user = await users_collection.find_one({"_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        updated_result = await users_collection.update_one(
            {"_id": user_id},
            {"$push": {"modules": module_id}}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if updated_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to add module to user")


async def get_module_by_id(module_id: str):
    await get_collection()

    try:
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid module_id")

    try:
        module = await modules_collection.find_one({"_id": module_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    return get_module_schema(module)


async def edit_module_func(module_id: str, module_title: str):
    await get_collection()
    try:
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid module_id")

    module = await modules_collection.find_one({"_id": module_id, "is_deleted": False})

    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    if not re.match('^[a-zA-Z0-9 ]*$', module_title):
        raise HTTPException(status_code=400, detail="Module title contains invalid characters")

    updated_result = await modules_collection.update_one(
        {"_id": module_id},
        {"$set": {"title": module_title}}
    )

    if updated_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to edit module")

    return {"message": "success", "detail": "Module edited successfully"}


async def delete_module_func(user_id: str, module_id: str):
    await get_collection()

    try:
        user_id = ObjectId(user_id)
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user_id or module_id")

    module = await modules_collection.find_one({"_id": module_id})
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    if module["title"].endswith("_other"):
        raise HTTPException(status_code=400, detail="Cannot delete other module")

    if not module["is_deleted"]:
        raise HTTPException(status_code=400, detail="Module is not trashed")

    for attempt in range(3):
        try:
            async with await client.start_session() as session:
                async with session.start_transaction():
                    for note_id in module["notes"]:
                        result = await notes_collection.delete_one({"_id": note_id}, session=session)
                        if result.deleted_count == 0:
                            raise HTTPException(status_code=500, detail="Failed to delete note")

                    result = await modules_collection.delete_one({"_id": module_id}, session=session)
                    if result.deleted_count == 0:
                        raise HTTPException(status_code=500, detail="Failed to delete module")

                    user_result = await users_collection.find_one_and_update(
                        {"_id": user_id},
                        {"$pull": {"modules": module_id}},
                        session=session
                    )

                    if user_result is None:
                        raise HTTPException(status_code=500, detail="Failed to delete module from user")

            return {"message": "success", "detail": "Module deleted successfully"}

        except errors.OperationFailure as e:
            if 'TransientTransactionError' in e.details.get('errorLabels', []):
                continue  # Retry the transaction
            else:
                raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=500, detail="Failed to delete module after multiple attempts")
