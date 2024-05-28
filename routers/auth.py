from fastapi import APIRouter, Body
from model.user import User, LoginUser
import controller.auth_controller as controller

router = APIRouter(
    prefix="/auth",
)

@router.post("/signup")
async def signup(user: User = Body(...)):
    try:
        res = await controller.signup_func(user)
        if res == "exist_user":
            return {"message": "exist_user"}
        else:
            return {"message": "successful", "user_id": res}
    except Exception as e:
        return {"error": str(e)}


@router.post("/login")
async def login(user: LoginUser = Body(...)):
    try:
        res = await controller.authenticate_user(user)
        if res == "incorrect_username":
            return {"message": "invalid", "reason": "incorrect_username"}
        elif res == "incorrect_password":
            return {"message": "invalid", "reason": "incorrect_password"}
        else:
            token = controller.signJWT(res["id"])
            return {"message": "valid", "user": res, "token": token}
    except Exception as e:
        return {"error": str(e)}


@router.post("/logout")
async def logout():
    return {"message": "logout"}
