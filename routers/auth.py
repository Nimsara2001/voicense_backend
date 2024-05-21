from fastapi import APIRouter, Body
from model.user import User

import controller.auth_controller as controller

router = APIRouter(
    prefix="/auth",
)


@router.post("/signup")
async def signup(user: User = Body(...)):
    try:
        user_id = await controller.signup_func(user)
        return {"message": "successful", "user_id": user_id}
    except Exception as e:
        return {"error": str(e)}


@router.post("/login")
async def login():
    return {"message": "Login page"}
