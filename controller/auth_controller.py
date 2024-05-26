from datetime import datetime
from typing import Dict
import time
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from db_config import get_db
from model.module import Module
from model.user import User, get_user_schema, LoginUser

JWT_SECRET_KEY = "Ks9Tz2Ld7Xv8Yw5Qr6Uj3Nb1Ec0Fm4Oa"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_collection = None
modules_collection = None


async def set_collection():
    global user_collection, modules_collection
    db = await get_db()

    if db is None:
        raise Exception("Failed to get database connection")

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
        return "exist_user"
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


async def authenticate_user(login_user: LoginUser):
    try:
        await set_collection()
        user = await user_collection.find_one({"username": login_user.username})
        if user is None:
            return "incorrect_username"
        else:
            if not verify_password(login_user.password, user["password"]):
                return "incorrect_password"
            return get_user_schema(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================================= JWT ==================================================

def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + JWT_ACCESS_TOKEN_EXPIRE * 60
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def verify_jwt(token: str) -> bool:
    is_token_valid: bool = False
    try:
        payload = decodeJWT(token)
    except:
        payload = None
    if payload:
        is_token_valid = True
    return is_token_valid
