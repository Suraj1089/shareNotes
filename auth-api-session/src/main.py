from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timedelta
from .api.schemas import User
from .api.database import database, users  # Update with the correct import statements
import secrets
from .api import hashing

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


async def get_user(email: str):
    query = users.select().where(users.c.email == email) # check user already exist with email
    return await database.fetch_one(query)


async def create_user(user: dict):
    print('inside create_user')
    print(user)
    user_copy = user.copy()
    api_key = secrets.token_hex(10)     # generate 10 digit token
    user_copy.update({"api_key": api_key})
    
    query = users.insert().values(
        username=user['username'],
        email=user['email'],
        expiry_date=datetime.now() + timedelta(days=365),
        api_key=hashing.get_password_hash(api_key)
    )
    user_ = await database.execute(query)
    # add user id to response
    user_copy.update({"id":user_})
    return user_copy


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: User):
    user_ = await get_user(user.email)
    print('users are', user_)
    if user_ is not None:
        print('error')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with email {user.email} already exists!'
        )
    print('user created')
    return await create_user(user.dict())


@app.post('/login')
def register():
    return {
        "data":"login"
    }


