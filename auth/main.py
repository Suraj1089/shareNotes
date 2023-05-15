from fastapi import FastAPI,Request,Depends,HTTPException,status
import uvicorn
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from . import schemas,models,hashing
from fastapi.middleware.cors import CORSMiddleware
from .database import engine,get_db
from sqlalchemy.orm import Session


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


@app.post('/login')
def login_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = get_user(request.email,db)
    print(user.email)
    if user is not None:
        return "return login token"
    return "user login"



if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)