from fastapi import FastAPI, HTTPException, status,Depends,Response
from datetime import datetime, timedelta

from fastapi.param_functions import Form
from .api.schemas import User,Token
from .api.database import database, users  # Update with the correct import statements
import secrets
from .api import hashing
from typing import Annotated, Dict, Optional
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
app = FastAPI()
from jose import JWTError, jwt

# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Home page
@app.get('/home')
def home():
    return {"data": "home page"}

@app.on_event("startup")
async def startup():
    # print('starting database')
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    # print('shutting down')
    await database.disconnect()


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


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: User):
    user_ = await get_user(user.email)
    print('users are', user_)
    if user_ is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with email {user.email} already exists!'
        )
    print('user created')
    return await create_user(user.dict())


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print('user')
    return credentials_exception



@app.post("/token",response_model=Token,status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],response:Response):
    user = await authenticate(form_data.username,form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user.username},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": token, "token_type": "bearer"}




@app.get("/getUserData", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
