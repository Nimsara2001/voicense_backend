from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import Dict, Optional
from db_config import get_db
from model.user_model import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "Ks9Tz2Ld7Xv8Yw5Qr6Uj3Nb1Ec0Fm4Oa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# MongoDB collection
db = get_db()
UserCollection = db["User"]

home_screens = Dict[str, str]
home_screens = {
    "lecturer": "lecturer_home",
    "student": "student_home",
}

# Define a dictionary to map user types to frontend URLs
frontend_urls: Dict[str, str] = {
    "lecturer": "https://your-app.com/lecturer_home",
    "student": "https://your-app.com/student_home",
}


async def get_user(username: str):
    return UserCollection.find_one({"username": username})


async def create_user(username: str, password: str, first_name: str, last_name: str, user_type: str):
    hashed_password = pwd_context.hash(password)
    user = {"username": username,
            "hashed_password": hashed_password, "first_name": first_name, "last_name": last_name, "user_type": user_type}
    result = UserCollection.insert_one(user)
    return User(**user, id=str(result.inserted_id))


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user["hashed_password"]):
        return False
    return User(**user)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Shorter expiration time for access tokens
        expire = datetime.utcnow() + timedelta(minutes=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    # Longer expiration time for refresh tokens
    expire = datetime.utcnow() + timedelta(days=32)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    # Fetch the user from the database
    user = await get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return User(**user)

# hansaka branch
