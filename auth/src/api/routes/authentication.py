from fastapi import Depends,HTTPException,status,Request
from ..utils import hashing
from ..db.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter

from ..db import models, schemas
from ..utils.token import (get_user,create_access_token,get_current_user,
                    update_user,
                    delete_user,
                    get_all_users,
                    get_user_by_email,)

# from ..settings.config import SALT


auth = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth.post('/register',response_model=schemas.User,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    """
        Create a new user
        user: schemas.UserCreate = pydantic model for user
    """
    user_in_db = db.query(models.User).filter(models.User.email == user.email)
    print(user_in_db.first())
    if user_in_db.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with {user.email} already exist")

    hashed_password = hashing.Hash.bcrypt(user.password)
    new_user = models.User(email=user.email,name=user.name,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth.post('/login',status_code=status.HTTP_200_OK)
def login_user(request: schemas.UserLogin, db: Session = Depends(get_db)):
    user = get_user(email=request.email,db=db)
    if not user:
        # raise error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
    if not hashing.Hash.verify(user.hashed_password,request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incorrect password"
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth.get('/user',status_code=status.HTTP_200_OK)
def get_current_logged_user(request: Request,db: Session = Depends(get_db)):
    # get token from header
    print(request.headers)
    token = request.headers.get("authorization")
    # get user from token
    user = get_current_user(token,db)
    return user


@auth.put('/user/{email}',status_code=status.HTTP_202_ACCEPTED)
def update_user_by_email(email: str,user: schemas.UserUpdate,db: Session = Depends(get_db)):
    return update_user(email,db,user)

@auth.delete('/user/{email}',status_code=status.HTTP_202_ACCEPTED)
def delete_user_by_email(email: str,db: Session = Depends(get_db)):
    return delete_user(email,db)

@auth.get('/users',status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@auth.get('/user/{email}',status_code=status.HTTP_200_OK)
def get_user_by_email(email: str,db: Session = Depends(get_db)):
    return get_user_by_email(email,db)





