from fastapi import APIRouter
import controller.module_controller as controller

router = APIRouter(
    prefix="/module"
)


@router.get("/all")
async def get_all_modules(user_id: str):
    try:
        modules = await controller.get_all_modules_func(user_id)
        return modules
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.post("/{module_id}/notes")
async def view_module_notes(module_id: str):
    try:
        notes = await controller.get_all_notes_of_module_func(module_id, False)
        return notes
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.post("/search")
async def search_module(search_text: str):
    try:
        search_results = await controller.search_module_func(search_text)
        return search_results
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.put("/trash/{module_id}")
async def trash_module(module_id: str):
    try:
        res = await controller.trash_module_func(module_id)
        return res
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.post("/other/notes")
async def view_other_module_notes(module_id: str):
    try:
        other_notes = await controller.get_all_notes_of_module_func(module_id, True)
        return other_notes
    except Exception as e:
        return {"message": "failed", "error": str(e)}


@router.post("/add")
async def add_module():
    # for testing
    return {"message": "Add module"}


@router.post("/edit/{module_id}")
async def edit_module(module_id: int):
    return {"message": f"Edit module {module_id}"}


@router.get("/share/{module_id}")
async def share_module(module_id: int):
    return {"message": f"Share module {module_id}"}
