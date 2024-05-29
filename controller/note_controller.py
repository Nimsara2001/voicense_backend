import datetime
from db_config import get_db
from fastapi import HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

notes_collection = None

async def get_collection():
    global notes_collection
    db = await get_db()
    notes_collection = db["Note"]

async def get_note_by_id(note_id: str):
    try:
        note=await get_note_and_update_last_accessed(note_id)
        if note:
            return note['content']
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:  # Add except clause
        raise HTTPException(status_code=500, detail=str(e))

# delete a note
async def delete_note_by_id_permanently(note_id: str):
    try:
        # Ensure collections are initialized
        if notes_collection is None:
            await get_collection()

        response = await notes_collection.find_one({"_id":ObjectId(note_id)})
        if response:
         if response['is_deleted'] == True:
             result = await notes_collection.delete_one({"_id": ObjectId(note_id)})
             if result.deleted_count == 1:
                return {"message": "Note deleted"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:  # Add except clause
        raise HTTPException(status_code=500, detail=str(e))
    
async def recently_accessed_notes():
    try:
        # Ensure collections are initialized
        if notes_collection is None:
            await get_collection()

        recent_notes=[]
        notes = notes_collection.find().sort([("last_accessed", -1)]).limit(3)
        async for note in notes:
            recent_notes.append(str(note["_id"]))
        # return recent_notes
        print(recent_notes)
        return recent_notes
    
    except Exception as e:  # Add except clause
        raise HTTPException(status_code=500, detail=str(e))    

async def get_note_and_update_last_accessed(note_id: str):
    try:
        # Ensure collections are initialized
        if notes_collection is None:
            await get_collection()

        note = await notes_collection.find_one_and_update(
            {"_id": ObjectId(note_id)},
            {"$set": {"last_accessed": datetime.datetime.now()}},
            return_document=True
        )
        if note:
            return note
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:  # Add except clause
        raise HTTPException(status_code=500, detail=str(e))


async def trash_note_by_id(note_id:str):
    try:
        if notes_collection is None:
            await get_collection()

        updated_result=notes_collection.update_one({"_id":ObjectId(note_id)},{"$set":{"is_deleted":True}})  
        if updated_result.modified_count == 1:
          return {"message": f"Item with ID {id} has been trashed"}
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")  

    except Exception as e:  # Add except clause
        raise HTTPException(status_code=500, detail=str(e))
    
async def restore_note_by_id(note_id:str):
    try:
        if notes_collection is None:
            await get_collection()
        
        updated_result= await notes_collection.update_one({"_id":ObjectId(note_id)},{"$set":{"is_deleted":False}})
        if updated_result.modified_count == 1 :
            return {"message": f"Item with ID {id} has been restored"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
