from fastapi import FastAPI, HTTPException, status,Depends
from datetime import datetime, timedelta
from .api.schemas import User
from .api.database import database, users  # Update with the correct import statements
import secrets
from .api import hashing
from typing import Annotated
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


async def get_user(email: str):
    query = users.select().where(users.c.email == email) # check user already exist with email
    return await database.fetch_one(query)


async def create_user(user: dict):
    api_key = secrets.token_hex(10)     # generate 10 digit token
    query = users.insert().values(
        username=user['username'],
        email=user['email'],
        expiry_date=datetime.now() + timedelta(days=365),
        api_key=hashing.get_password_hash(api_key)
    )
    user_ = await database.execute(query)
    return api_key


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
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     username: str = payload.get("sub")
    #     if username is None:
    #         raise credentials_exception
    #     token_data = TokenData(username=username)
    # except JWTError:
    #     raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {
        "user":"login"
    }
    # user_dict = fake_users_db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    # return {"access_token": user.username, "token_type": "bearer"}



@app.get("getUserData", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
