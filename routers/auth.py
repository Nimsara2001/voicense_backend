from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/auth",
)

@router.post("/signup")
async def signup():
    return await {"message": "Signup page"}

@router.post("/login")
async def login():
    return {"message": "Login page"}

#mihin branch