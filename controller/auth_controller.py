from datetime import datetime
from passlib.context import CryptContext
from fastapi import HTTPException
from db_config import get_db
from model.module import Module
from model.user import User, get_user_schema

SECRET_KEY = "Ks9Tz2Ld7Xv8Yw5Qr6Uj3Nb1Ec0Fm4Oa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_collection = None
modules_collection = None


async def set_collection():
    global user_collection, modules_collection
    db = await get_db()

    if user_collection is None:
        user_collection = db["User"]

    if modules_collection is None:
        modules_collection = db["Module"]


async def exist_user(username: str) -> bool:
    await set_collection()
    user = await user_collection.find_one({"username": username})
    return user is not None


async def init_other_module(username: str):
    await set_collection()
    current_date = datetime.now().date()
    current_timestamp = datetime.now()
    new_module = Module(
        title=f"{username}_other",
        created_date=str(current_date),
        last_accessed=str(current_timestamp),
    )
    result = await modules_collection.insert_one(new_module.dict())
    return result.inserted_id


async def signup_func(user: User):
    await set_collection()
    user.password = get_password_hash(user.password)
    if await exist_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    else:
        other_module_id = await init_other_module(user.username)
        user.modules.append(other_module_id)
        try:
            result = await user_collection.insert_one(user.dict())
            if result.inserted_id is None:
                raise HTTPException(status_code=500, detail="User insertion failed")
            return str(result.inserted_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
