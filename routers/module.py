from fastapi import APIRouter
import controller.module_controller as controller
from model.module import Module, DeleteModuleRequest

router = APIRouter(
    prefix="/module"
)

@router.get("/all")  # other module retrieved.can extract in frontend.
async def get_all_modules(user_id: str):
    print("all accessed------------")
    modules = await controller.get_all_modules_func(user_id)
    print(modules)
    return modules

@router.get("/trashed")
async def get_all_trashed_modules(user_id: str):
    modules = await controller.get_all_trashed_modules(user_id)
    return modules


@router.post("/{module_id}/notes")   #methana get method ekak nedamo
async def view_module_notes(module_id: str):
    notes = await controller.get_all_notes_of_module_func(module_id)
    return notes


@router.post("/search")  # search can implement in frontend also.
async def search_module(user_id: str, search_text: str):
    search_results = await controller.search_module_func(user_id, search_text)
    return search_results


@router.post("/trash/{module_id}")
async def trash_module(module_id: str):
    res = await controller.trash_and_restore_module_func(module_id, True)
    return res


@router.post("/restore/{module_id}")
async def restore_module(module_id: str):
    print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
    print(module_id)
    res = await controller.trash_and_restore_module_func(module_id, False)
    print("restore",res)
    return res


@router.post("/delete")
async def delete_module(request: DeleteModuleRequest):
    print("delete",request.module_id)
    res = await controller.delete_module_func(request.user_id, request.module_id)
    return res


@router.post("/add")
async def add_module(user_id: str,title: str):
    res = await controller.add_module_func(title, user_id)
    return res


@router.post("/edit/{module_id}")
async def edit_module(module_id: str, module_title: str):
    res = await controller.edit_module_func(module_id, module_title)
    return res


@router.get("/share/{module_id}") # implement later
async def share_module(module_id: int):
    return {"message": f"Share module {module_id}"}
