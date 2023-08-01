from ..db import models
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from jose import jwt,JWTError
from fastapi import HTTPException,status
from ..db import schemas

from ..settings import config



def get_user(email: str,db: Session,password: str = True):
    if password:
        user = db.query(models.User).filter(models.User.email == email)
    else:
        user = db.query(models.User).with_entities(models.User.email,models.User.name).filter(models.User.email == email)
    if user.first():
        return user.first() 
    return None

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str,db: Session):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        print(email)
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=email)
        print(token_data)
        user = get_user(email=token_data.username,db=db,password=False)
        print(user)
        if user is None:
            raise credentials_exception
        data = {
            "email": user[0],
            "name": user[1]
        }
        return data
    except JWTError:
        raise credentials_exception


def update_user(email: str,db: Session,user: schemas.UserUpdate):
    user_in_db = db.query(models.User).filter(models.User.email == email)
    if user_in_db.first():
        user_in_db.update(user)
        db.commit()
        return {"message": "User updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {email} not found")

def delete_user(email: str,db: Session):
    user_in_db = db.query(models.User).filter(models.User.email == email)
    if user_in_db.first():
        user_in_db.delete()
        db.commit()
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {email} not found")

def get_all_users(db: Session):
    users = db.query(models.User).all()
    return users

def get_user_by_email(email: str,db: Session):
    user = db.query(models.User).filter(models.User.email == email)
    if user.first():
        return user.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {email} not found")

