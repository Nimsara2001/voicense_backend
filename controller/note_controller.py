from datetime import datetime
import re

from db_config import get_db, client
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

from model.note import Note, get_note_schema
from model.transcription import Transcription

notes_collection = None
transcriptions_collection = None
modules_collection = None
users_collection = None
recentNotes_collection = None



async def get_collection():
    global notes_collection, transcriptions_collection, modules_collection, users_collection,recentNotes_collection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")

    if notes_collection is None:
        notes_collection = db["Note"]

    if transcriptions_collection is None:
        transcriptions_collection = db["Transcription"]

    if modules_collection is None:
        modules_collection = db["Module"]

    if users_collection is None:
        users_collection = db["User"]

    if recentNotes_collection is None:
        recentNotes_collection = db["RecentNotes"]     


# async def recently_accessed_notes(user_id: str):
#     await get_collection()

#     try:
#         user_id = ObjectId(user_id)
#     except InvalidId:
#         raise HTTPException(status_code=400, detail="Invalid user_id")

#     pipeline = [
#         {"$match": {"_id": user_id}},
#         {"$unwind": "$modules"},
#         {"$lookup": {
#             "from": "Module",
#             "localField": "modules",
#             "foreignField": "_id",
#             "as": "module"
#         }},
#         {"$unwind": "$module"},
#         {"$match": {"module.is_deleted": False}},
#         {"$unwind": "$module.notes"},
#         {"$lookup": {
#             "from": "Note",
#             "localField": "module.notes",
#             "foreignField": "_id",
#             "as": "note"
#         }},
#         {"$unwind": "$note"},
#         {"$match": {"note.is_deleted": False}},
#         {"$sort": {"note.last_accessed": -1}},
#         {"$limit": 10}
#     ]

#     recent_notes_cursor = users_collection.aggregate(pipeline)
#     recent_notes = await recent_notes_cursor.to_list(length=100)

#     if not recent_notes:
#         raise HTTPException(status_code=404, detail="No notes found")

#     recent_notes = [get_note_schema(note["note"]) for note in recent_notes]

#     return recent_notes

async def recently_accessed_notes(user_id: str):
    await get_collection()
    try:
        user_id=ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid userId")
    
    try:
        recent_notes_list=[]
        document = await recentNotes_collection.find_one({"userId":str(user_id)})
        recent_notes=document["notes"]
        for note_id in recent_notes:
            try:
                note_id=ObjectId(note_id)
            except InvalidId:
                raise HTTPException(status_code=400, detail="Invalid note_id")  
              
            note=await notes_collection.find_one({"_id":note_id})
            recent_notes_list.append(get_note_schema(note))
        print(recent_notes_list)    
        return recent_notes_list
    
    except Exception as e:
        raise HTTPException(status_code=404,detail="Notes not found")


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
        # await update_last_accessed(str(note_id))
        return get_note_schema(note)
    else:
        raise HTTPException(status_code=404, detail="Note not found")

async def get_all_trashed_notes(user_id:str):
    await get_collection()
    try:
        user_id = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    user=await users_collection.find_one({"_id":user_id});    

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    trash_notes=[]
    for module_id in user["modules"]:
        module=await modules_collection.find_one({"_id":module_id,"is_deleted":False})
        for note_id in module["notes"]:
            note=await notes_collection.find_one({"_id":note_id,"is_deleted":True})
            if note is not None:
                trashed_note=get_note_schema(note)
                trashed_note["module_id"]=str(module_id)
                trash_notes.append(trashed_note)

    if not trash_notes:
        raise HTTPException(status_code=404, detail="No trashed notes found")      
    return trash_notes
      

# async def update_last_accessed(note_id: str):
#     await get_collection()
#     try:
#         note_id = ObjectId(note_id)
#     except InvalidId:
#         raise HTTPException(status_code=400, detail="Invalid note_id")

#     updated_result = await notes_collection.update_one(
#         {"_id": note_id, "is_deleted": False},
#         {"$set": {"last_accessed": str(datetime.now())}}
#     )

#     if updated_result.modified_count == 1:
#         return {"message": "success", "detail": f"Note with ID {note_id} last accessed updated"}
#     else:
#         raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

async def insert_to_recentNoteList(userId:str,note_id: str):
    await get_collection()
    try:
        userId = ObjectId(userId)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid userId")    
    
    MAX_LENGTH = 10
    user_document = await recentNotes_collection.find_one({"userId":userId})
    if user_document is not None:
     updated_notes = user_document["notes"].append(note_id)
     if len(updated_notes) > MAX_LENGTH:
        updated_notes = updated_notes - updated_notes[:len(updated_notes) - MAX_LENGTH]
     updated_notes_list = await recentNotes_collection.update_one({"userId":userId},{"$set":{"notes":updated_notes}})
     if updated_notes_list.modified_count == 1:
        return {"message": "success", "detail": f"Note with ID {note_id} inserted to the list"}       
     else:
        raise HTTPException(status_code=404, detail=f"User with ID {userId} not found")
    
         
async def trash_and_restore_note_by_id(note_id: str, is_trash: bool):
    await get_collection()
    try:
        note_id = ObjectId(note_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id")

    updated_result = await notes_collection.update_one({"_id": note_id}, {"$set": {"is_deleted": is_trash}})

    if updated_result.modified_count == 1:
        action = "trashed" if is_trash else "restored"
        return {"message": "success", "detail": f"Note with ID {note_id} has been {action}"}
    else:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


async def delete_note_by_id_permanently(module_id: str, note_id: str):
    await get_collection()
    try:
        note_id = ObjectId(note_id)
        module_id = ObjectId(module_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid note_id or module_id")

    async with await client.start_session() as sdt:
        sdt.start_transaction()

        try:
            result = await notes_collection.delete_one({"_id": note_id, "is_deleted": True}, session=sdt)

            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Note is not found")

            module = await modules_collection.find_one({"_id": module_id})

            if module is None:
                raise HTTPException(status_code=404, detail="Module not found")

            updated_result = await modules_collection.update_one(
                {"_id": module_id},
                {"$pull": {"notes": note_id}}
            )

            if updated_result.modified_count == 1:
                sdt.commit_transaction()
                return {"message": "success", "detail": "Note has been deleted permanently"}

        except Exception as e:
            sdt.abort_transaction()
            raise HTTPException(status_code=500, detail=str(e))


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
