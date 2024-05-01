from fastapi import APIRouter

router = APIRouter(
    prefix="/module",
)


@router.get("/all")
async def get_all_modules():
    return {"message": "Get all modules"}


@router.post("/search")
async def search_module():
    return {"message": "Search module"}


@router.get("/share/{module_id}")
async def share_module(module_id: int):
    return {"message": f"Share module {module_id}"}


@router.delete("/trash/{module_id}")
async def trash_module(module_id: int):
    return {"message": f"Trash module {module_id}"}


@router.post("/{module_id}/notes")
async def view_module_notes(module_id: int):
    return {"message": f"view module notes {module_id}"}


@router.get("/other/notes")
async def view_other_module_notes():
    return {"message": "Other module notes"}


@router.post("/add")
async def add_module():
    return {"message": "Add module"}


@router.post("/edit/{module_id}")
async def edit_module(module_id: int):
    return {"message": f"Edit module {module_id}"}