from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from .config import ALGORITHM, SECRET_KEY
from .hashing import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_username(username: str) -> Optional[UserInDB]:
    for user in database:
        if user.username == username:
            return user
    return None


def create_user(user: User) -> UserInDB:
    hashed_password = get_password_hash(user.username)
    user_data = UserInDB(**user.dict(), hashed_password=hashed_password)
    database.append(user_data)
    return user_data


def authenticate_user(api_key: str) -> Optional[UserInDB]:
    for user in database:
        if user.hashed_password == api_key:
            return user
    return None


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt