from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException,status
from jose import JWTError, jwt
from .config import ALGORITHM, SECRET_KEY
from .import hashing
from .database import database, users
import secrets
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")



async def get_user(email: str):
    query = users.select().where(users.c.email == email) # check user already exist with email
    return await database.fetch_one(query)

async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)

async def create_user(user: dict):
    user_copy = user.copy()
    api_key = secrets.token_hex(10)     # generate 10 digit token
    user_copy.update({'api_key': api_key})
    hashed_key = hashing.get_password_hash(api_key)
    query = users.insert().values(
        username=user['username'],
        email=user['email'],
        expiry_date=datetime.now() + timedelta(days=365),
        api_key=hashed_key
    )
    user_ = await database.execute(query)
    user_copy.update({'id': user_})
    return user_copy

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not hashing.verify_password(password, user['api_key']):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.username)
    if user is None:
        raise credentials_exception
    print("user in current user ", user)
    return user


