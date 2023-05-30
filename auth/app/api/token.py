from app.api import models,config
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from jose import jwt



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