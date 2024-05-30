from datetime import datetime
from db_config import get_db
from fastapi import HTTPException
from bson import ObjectId

from model.note import Note
from model.transcription import Transcription

notes_collection = None
transcriptions_collection = None
modules_collection = None


async def get_collection():
    global notes_collection, transcriptions_collection, modules_collection
    db = await get_db()
    notes_collection = db["Note"]
    transcriptions_collection = db["Transcription"]
    modules_collection = db["Module"]


async def get_note_by_id(note_id: str):
    try:
        note = await get_note_and_update_last_accessed(note_id)
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

        response = await notes_collection.find_one({"_id": ObjectId(note_id)})
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

        recent_notes = []
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


async def trash_note_by_id(note_id: str):
    try:
        if notes_collection is None:
            await get_collection()

        updated_result = notes_collection.update_one({"_id": ObjectId(note_id)}, {"$set": {"is_deleted": True}})
        if updated_result.modified_count == 1:
            return {"message": f"Item with ID {id} has been trashed"}
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")

    except Exception as e:  # Add except clause
        raise HTTPException(status_code=500, detail=str(e))


async def restore_note_by_id(note_id: str):
    try:
        if notes_collection is None:
            await get_collection()

        updated_result = await notes_collection.update_one({"_id": ObjectId(note_id)}, {"$set": {"is_deleted": False}})
        if updated_result.modified_count == 1:
            return {"message": f"Item with ID {id} has been restored"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def save_note_and_transcription(note, transcription, module_id):
    try:
        if notes_collection is None:
            await get_collection()
        if transcriptions_collection is None:
            await get_collection()

        new_note = Note(
            title=note["title"],
            description="Sample description",
            content=note["content"],
            created_date=str(datetime.now()),
            last_accessed=str(datetime.now()),
        )
        note_result = await notes_collection.insert_one(new_note.dict())
        if note_result.inserted_id is None:
            raise HTTPException(status_code=500, detail="Note insertion failed")

        new_transcription = Transcription(
            content=transcription,
            generated_date=str(datetime.now()),
            note_id=ObjectId(note_result.inserted_id),
        )

        transcription_result = await transcriptions_collection.insert_one(new_transcription.dict())
        if transcription_result.inserted_id is None:
            raise HTTPException(status_code=500, detail="Transcription insertion failed")

        await add_note_to_module(note_result.inserted_id, module_id)

        return {"message": "success", "note_id": str(note_result.inserted_id),
                "transcription_id": str(transcription_result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from bson.errors import InvalidId

async def add_note_to_module(note_id, module_id):
    try:
        # Ensure collections are initialized
        if notes_collection is None or modules_collection is None:
            await get_collection()

        # Validate note_id and module_id
        try:
            note_id = ObjectId(note_id)
            module_id = ObjectId(module_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid note_id or module_id")

        # Find the module with the given module_id
        module = await modules_collection.find_one({"_id": module_id})

        # If the module is not found, raise an HTTPException
        if module is None:
            raise HTTPException(status_code=404, detail="Module not found")

        # Add the note_id to the module's notes list
        updated_result = await modules_collection.update_one(
            {"_id": module_id},
            {"$push": {"notes": note_id}}
        )

        # If the module was not updated, raise an HTTPException
        if updated_result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to add note to module")

        return {"message": f"Note with ID {note_id} has been added to module with ID {module_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
