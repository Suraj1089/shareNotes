from fastapi import FastAPI, HTTPException, status,Depends
from datetime import datetime, timedelta

from fastapi.param_functions import Form
from .api.schemas import User
from .api.database import database, users  # Update with the correct import statements
import secrets
from .api import hashing
from typing import Annotated, Dict, Optional
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
app = FastAPI()


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


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(self, api_key: str | None = None):
        super().__init__(grant_type="password",  username=api_key, password="")

class customOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str):
        super().__init__(tokenUrl)

async def get_user(email: str):
    query = users.select().where(users.c.email == email) # check user already exist with email
    return await database.fetch_one(query)

async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)

async def create_user(user: dict):
    api_key = secrets.token_hex(10)     # generate 10 digit token
    query = users.insert().values(
        username=user['username'],
        email=user['email'],
        expiry_date=datetime.now() + timedelta(days=365),
        api_key=api_key
    )
    user_ = await database.execute(query)
    return api_key

async def authenticate(api_key: str):
    query = users.select().where(users.c.api_key == api_key)
    return await database.fetch_one(query)


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


oauth2_scheme = customOAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print('user')
    return credentials_exception



@app.post("/token")
async def login(form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()]):
    print(form_data.username)
    user = await authenticate("f44a025c991a2d0df905")
    users = await get_all_users()
    print("user in login",user)
    return {
        "user":users
    }



@app.get("getUserData", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
