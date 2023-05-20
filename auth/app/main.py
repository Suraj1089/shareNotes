from fastapi import FastAPI,Request,Depends,HTTPException,status
import uvicorn
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from app.api import schemas,models,hashing,config
from fastapi.middleware.cors import CORSMiddleware
from app.api.database import engine,get_db
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from jose import JWTError,jwt
import json
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/register',response_model=schemas.User)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    user_in_db = db.query(models.User).filter(models.User.email == user.email)
    if user_in_db.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with {user.email} already exist")
    hashed_password = hashing.Hash.bcrypt(user.password)
    new_user = models.User(email=user.email,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(email: str,db: Session):
    user = db.query(models.User).filter(models.User.email == email)
    if user.first():
        return user.first() 
    return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

@app.post('/login',status_code=status.HTTP_200_OK)
def login_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = get_user(request.email,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)