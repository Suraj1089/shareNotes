from fastapi import Depends,HTTPException,status
from app.api import schemas,models,hashing
from app.api.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter
from .token import get_user,create_access_token


auth = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth.post('/register',response_model=schemas.User,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    """
        Create a new user
        user: schemas.UserCreate = pydantic model for user
    """
    user_in_db = db.query(models.User).filter(models.User.email == user.email)
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
    user = get_user(request.email,db)
    if not user:
        # raise error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth.get('/users',status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
    return user