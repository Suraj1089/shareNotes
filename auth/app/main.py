from fastapi import FastAPI,Request,Depends,HTTPException,status
from app.api import schemas,models,hashing,config
from fastapi.middleware.cors import CORSMiddleware
from app.api.database import engine,get_db
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from jose import JWTError,jwt
from app.api import routes
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=routes.auth)