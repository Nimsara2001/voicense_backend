from fastapi import APIRouter
import controller.module_controller as controller

router = APIRouter(
    prefix="/module",
)


@router.get("/all")
async def get_all_modules(user_id: str):
    modules = controller.get_all_modules_func(user_id)
    return {"message": modules}


@router.get("/titles")
async def get_all_modules_titles(user_id: str):
    modules = controller.get_all_modules_titles_func(user_id)
    return {"message": modules}


# done


@router.post("/search")
async def search_module(search_text):
    search_results = controller.search_module_func(search_text)
    return {"message": search_results["message"]}  # Access "message" key directly


# modify

@router.get("/share/{module_id}")
async def share_module(module_id: int):
    return {"message": f"Share module {module_id}"}


@router.delete("/trash/{module_id}")
async def trash_module(module_id: str):
    controller.trash_module_func(module_id)
    return {"message": f"Trash module {module_id}"}


# done

@router.post("/{module_id}/notes")
async def view_module_notes(module_id: str):
    notes = controller.get_all_notes_func(module_id)
    return {"message": notes}


@router.get("/other/notes")
async def view_other_module_notes(module_id: str):
    other_notes = controller.get_other_module_notes_func(module_id)
    return {"message": other_notes}


@router.post("/add")
async def add_module():
    # for testing
    return {"message": "Add module"}


@router.post("/edit/{module_id}")
async def edit_module(module_id: int):
    return {"message": f"Edit module {module_id}"}
