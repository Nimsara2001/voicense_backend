from db_config import get_db
from fastapi import HTTPException

modules_collection = None
notes_collection = None


async def get_collection():
    global modules_collection
    global notes_collection
    db = await get_db()
    modules_collection = db["Module"]
    notes_collection = db["Note"]


def get_all_modules_func(user_id: str):
    try:
        # Search by module_id using a filter with exact match
        find_results = modules_collection.find({"user_id": user_id})

        # Get the count of matching documents
        num_modules = modules_collection.count_documents({"user_id": user_id})

        # Raise an exception if no notes found
        if num_modules == 0:
            raise HTTPException(status_code=404, detail="No modules found for the specified user_id")

        # Initialize an empty list to store selected characteristics
        selected_characteristics = []

        # Extract desired fields from each document
        for module in find_results:
            selected_fields = {
                "module_id": module.get("module_id"),
                "title": module.get("title"),
                "created_date": module.get("created_date")
            }
            selected_characteristics.append(selected_fields)

        return selected_characteristics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def search_module_func(text: str):
    try:
        # Search within "module_title" field
        # search_query = {"module_id": {"$regex": text, "$options": "i"}, "_id": 0}
        # cursor = modules_collection.find(search_query)
        retrieved = modules_collection.find_one({"module_id": text})
        # Convert cursor to list of dictionaries
        print("this is the text")
        print(text)
        results = [document for document in retrieved]
        print("this is result")
        print(results)
        return {"message": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def trash_module_func(module_id: str):
    try:
        delete_result = modules_collection.delete_one({"module_id": module_id})
        if delete_result.deleted_count == 1:
            return {"message": "Module deleted successfully"}
        else:
            return {"message": "Module not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_all_notes_func(module_id: str):
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


def get_all_modules_titles_func(user_id: str):
    try:
        # Search by module_id using a filter with exact match
        find_results = modules_collection.find({"user_id": user_id})

        # Get the count of matching documents
        num_modules = modules_collection.count_documents({"user_id": user_id})

        # Raise an exception if no notes found
        if num_modules == 0:
            raise HTTPException(status_code=404, detail="No modules found for the specified user_id")

        # Initialize an empty list to store selected characteristics
        selected_characteristics = []

        # Extract desired fields from each document
        for module in find_results:
            selected_fields = {
                module.get("module_id"),
                module.get("title"),
            }
            selected_characteristics.append(selected_fields)

        return selected_characteristics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/get_mod_id")
# async def get_module(module_name: str):
#     module = modules_collection.find_one({'module_name': module_name})
