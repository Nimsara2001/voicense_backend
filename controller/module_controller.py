from db_config import get_db
from fastapi import HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

modules_collection = None
notes_collection = None
users_collection = None


async def get_collection():
    global modules_collection
    global notes_collection
    global users_collection
    db = await get_db()
    modules_collection = db["Module"]
    notes_collection = db["Note"]
    users_collection = db["User"]


async def get_all_modules_func(user_object_id: str):
    try:
        # Ensure collections are initialized
        if modules_collection is None or notes_collection is None or users_collection is None:
            await get_collection()

        user_id = ObjectId(user_object_id)
        # Search by module_id using a filter with exact match
        user = await users_collection.find_one({"_id": user_id})
        if user:
            # Convert ObjectIds to strings
            modules_data = []
            for module_id in user["modules"]:
                module = await modules_collection.find_one({"_id": module_id})
                if module:
                    module_data = jsonable_encoder(module)
                    modules_data.append(module_data)
            return modules_data
        else:
            print("no user is found")
            return None
    except Exception as e:
        # Handle exceptions gracefully
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_modules_titles_func(user_object_id: str):
    try:
        if modules_collection is None or notes_collection is None or users_collection is None:
            await get_collection()
        user_id = ObjectId(user_object_id)
        # Search by module_id using a filter with exact match
        user = await users_collection.find_one({"_id": user_id})
        data_retrieved = []
        print("1st step done")
        if user:
            # Convert ObjectIds to strings
            for module_id in user["modules"]:
                data_retrieved.append(str(module_id))
        modules = data_retrieved
        print("2nd step done")
        print(modules)
        if modules:
            titles_retrieved = []
            for module in modules:
                module_object_id = ObjectId(module)
                print("searching for...")
                print(module_object_id)
                module_object = await modules_collection.find_one({"_id": module_object_id})
                titles_retrieved.append(module_object["title"])
                print("3rd step done")
                print(titles_retrieved)
            return titles_retrieved
        else:
            print("no modules are found")
            return None
    except Exception as e:
        # Handle exceptions gracefully
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_notes_func(user_object_id: str, relevant_module_id: str):
    try:
        if modules_collection is None or notes_collection is None or users_collection is None:
            await get_collection()
        user_id = ObjectId(user_object_id)
        # Search by module_id using a filter with exact match
        user = await users_collection.find_one({"_id": user_id})
        data_retrieved = []
        print("1st step done")
        if user:
            # Convert ObjectIds to strings
            for module_id in user["modules"]:
                data_retrieved.append(str(module_id))
        modules = data_retrieved
        print("2nd step done")
        print(modules)
        if modules:
            titles_retrieved = []
            for module in modules:
                if (module == relevant_module_id):
                    module_object_id = ObjectId(module)
                    module_object = await modules_collection.find_one({"_id": module_object_id})
                    if module_object:
                        # Convert ObjectIds to strings
                        note_ids_retrieved = []
                        for note_id in module_object["notes"]:
                            note_ids_retrieved.append(str(note_id))
                        return note_ids_retrieved
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# TODO
def search_module_func(text: str):
    try:
        # Search within "module_title" field
        # search_query = {"module_id": {"$regex": text, "$options": "i"}, "_id": 0}
        # cursor = modules_collection.find(search_query)
        retrieved = modules_collection.find_one({"titles": text})
        # Convert cursor to list of dictionaries
        print("this is the text")
        print(text)
        results = [document for document in retrieved]
        print("this is result")
        print(results)
        return {"message": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# TODO
def trash_module_func(module_object_id: str):
    try:
        delete_result = modules_collection.delete_one({"module_id": module_object_id})
        if delete_result.deleted_count == 1:
            return {"message": "Module deleted successfully"}
        else:
            return {"message": "Module not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# TODO
def get_other_module_notes_func(module_id: str):
    try:
        # Search by module_id using a filter with exact match
        find_results = notes_collection.find({"module_id": module_id})

        # Get the count of matching documents
        num_notes = notes_collection.count_documents({"module_id": module_id})

        # Raise an exception if no notes found
        if num_notes == 0:
            raise HTTPException(status_code=404, detail="No notes found for the specified module_id")

        # Initialize an empty list to store selected characteristics
        selected_characteristics = []

        # Extract desired fields from each document
        for note in find_results:
            selected_fields = {
                note.get("title"),
                note.get("created_date"),
                note.get("description")
            }
            selected_characteristics.append(selected_fields)

        return selected_characteristics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/get_mod_id")
# async def get_module(module_name: str):
#     module = modules_collection.find_one({'module_name': module_name})

