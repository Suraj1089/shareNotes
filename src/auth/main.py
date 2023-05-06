from fastapi import FastAPI,Request,Depends,HTTPException
import uvicorn
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from models import User


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
   

if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)