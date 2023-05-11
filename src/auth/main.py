from fastapi import FastAPI,Request,Depends,HTTPException
import uvicorn
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from models import User
from routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)