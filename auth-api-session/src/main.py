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


