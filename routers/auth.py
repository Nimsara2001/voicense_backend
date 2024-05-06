from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
)


@router.post("/signup")
async def signup():
    return {"message": "Signup page"}


@router.post("/login")
async def login():
    return {"message": "Login page"}

