from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from databases import Database
from urllib.parse import quote_plus
import os
from typing import List
import sqlalchemy

app = FastAPI()

# POSTGRES CONFIGURATION


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./auth.db"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "auth_users",
    metadata,
    sqlalchemy.Column("email", sqlalchemy.String,primary_key=True),
    sqlalchemy.Column("user_name", sqlalchemy.String),
    sqlalchemy.Column("expiry_date", sqlalchemy.DateTime)
)


notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)




class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


bearer_scheme = HTTPBearer()


# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    email: str


class UserInDB(User):
    hashed_password: str




# async def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


# async def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# async def get_user_by_username(username: str) -> UserInDB:
#     await database.connect()
#     query = "SELECT * FROM auth_users WHERE username=%(username)s"
#     user_data = await database.fetch_one(query=query, values={"username": username})
#     await database.disconnect()
#     if user_data:
#         return UserInDB(
#             username=user_data["username"],
#             email=user_data["email"],
#             expiry_date=datetime.fromisoformat(user_data["expiry_date"]) if user_data["expiry_date"] else None,
#             hashed_password=user_data["hashed_password"],
#         )
#     return None


# async def create_user(user: User) -> UserInDB:
#     hashed_password = await get_password_hash(user.username)
#     await database.connect()
#     query = """
#         INSERT INTO auth_users (username, email, expiry_date, api_key)
#         VALUES (%(username)s, %(email)s, %(expiry_date)s, %(hashed_password)s)
#     """
#     values = {
#         "username": user.username,
#         "email": user.email,
#         "expiry_date": datetime.now() + timedelta(days=365),
#         "api_key": hashed_password,
#     }
#     await database.execute(query=query, values=values)
#     await database.disconnect()
#     return UserInDB(username=user.username, email=user.email, expiry_date=user.expiry_date, hashed_password=hashed_password)


# async def authenticate_user(username: str, password: str) -> UserInDB:
#     user = await get_user_by_username(username)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid username or password.")
#     if not await verify_password(password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid username or password.")
#     return user


# def create_access_token(data: dict, expires_delta: timedelta) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def decode_access_token(token: str) -> dict:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token.")


# @app.post("/register")
# async def register(user: User):
#     existing_user = await get_user_by_username(user.username)
#     print(existing_user)
#     # if existing_user:
#     #     raise HTTPException(status_code=400, detail="User already registered.")
#     # user_data = await create_user(user)
#     # return {"message": "User registered successfully.", "user": user_data}


# @app.post("/user/authenticate")
# async def authenticate(credentials: HTTPAuthorizationCredentials):
#     if credentials.scheme.lower() != "basic":
#         raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
#     username, password = credentials.credentials.split(":")
#     user = await authenticate_user(username, password)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     response = {"access_token": access_token, "token_type": "bearer"}
#     return response


# @app.get("/getUserData")
# async def get_user_data(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
#     if credentials.scheme.lower() != "bearer":
#         raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
#     token = credentials.credentials
#     payload = decode_access_token(token)
#     username = payload.get("sub")
#     user = await get_user_by_username(username)
#     if not user:
#         raise HTTPException(status_code=400, detail="User does not exist.")
#     return {"username": user.username, "email": user.email}


# @app.get("/protected")
# async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
#     if credentials.scheme.lower() != "bearer":
#         raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
#     token = credentials.credentials
#     payload = decode_access_token(token)
#     username = payload.get("sub")
#     user = await get_user_by_username(username)
#     if not user:
#         raise HTTPException(status_code=400, detail="User does not exist.")
#     return {"message": f"Welcome, {user.username}"}

# @app.get('/getallltables')
# async def get_all_tables():
#     await database.connect()
#     query = "SHOW TABLES"
#     tables = await database.fetch_all(query=query)
#     await database.disconnect()
#     return tables