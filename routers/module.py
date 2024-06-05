from fastapi import APIRouter
import controller.module_controller as controller
from model.module import Module

router = APIRouter(
    prefix="/module"
)


@router.get("/all")
async def get_all_modules(user_id: str):
    modules = await controller.get_all_modules_func(user_id)
    return modules


@router.post("/{module_id}/notes")
async def view_module_notes(module_id: str):
    notes = await controller.get_all_notes_of_module_func(module_id, False)
    return notes


@router.post("/search")
async def search_module(search_text: str):
    search_results = await controller.search_module_func(search_text)
    return search_results


@router.put("/trash/{module_id}")
async def trash_module(module_id: str):
    res = await controller.trash_module_func(module_id)
    return res


@router.post("/other/notes")
async def view_other_module_notes(module_id: str):
    other_notes = await controller.get_all_notes_of_module_func(module_id, True)
    return other_notes


@router.post("/add")
async def add_module(user_id: str, module: Module):
    res = await controller.add_module_func(module, user_id)
    return res


@router.post("/edit/{module_id}")
async def edit_module(module_id: str):
    res = await controller.edit_module_func(module_id)
    return res


@router.get("/share/{module_id}")
async def share_module(module_id: int):
    return {"message": f"Share module {module_id}"}
