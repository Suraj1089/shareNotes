from app.api import models,config,schemas
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from jose import jwt,JWTError
from fastapi import HTTPException,status



def get_user(email: str,db: Session,password: str = True):
    if password:
        user = db.query(models.User).filter(models.User.email == email)
    else:
        user = db.query(models.User).with_entities(models.User.email,models.User.name).filter(models.User.email == email)
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


def get_current_user(token: str,db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    # Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdXJhanBpc2FsMTEzQGdtYWlsLmNvbSIsImV4cCI6MTY4NTUzMDkwN30.cUIlyteNmxAOPWsCVP27xcMcT9BDKZrXzacc9WVYAq4
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
        # print(e)
        raise credentials_exception