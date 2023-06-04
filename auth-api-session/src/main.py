from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from .api.auth import auth
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



app = FastAPI()
app.include_router(auth)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}