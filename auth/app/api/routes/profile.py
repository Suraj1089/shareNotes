from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import schemas
from ..utils.utils import (create_profile,
                            get_profile,
                            update_profile,
                            delete_profile)



profile = APIRouter(
    prefix='/profile',
    tags=['Profile']
)


@profile.post('/user',status_code=status.HTTP_201_CREATED)
def create_profile(profile: schemas.ProfileCreate,db: Session = Depends(get_db)):
    return create_profile(db,profile)

@profile.get('/user/{email}',status_code=status.HTTP_200_OK)
def get_profile_by_email(email: str,db: Session = Depends(get_db)):
    return get_profile(db,email)

@profile.put('/user/{email}',status_code=status.HTTP_202_ACCEPTED)
def update_profile_by_email(email: str,profile: schemas.ProfileUpdate,db: Session = Depends(get_db)):
    return update_profile(db,email,profile)

@profile.delete('/user/{email}',status_code=status.HTTP_202_ACCEPTED)
def delete_profile_by_email(email: str,db: Session = Depends(get_db)):
    return delete_profile(email,db)
