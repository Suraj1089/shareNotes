from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from ..db import models,schemas



def create_profile(db: Session,profile: schemas.ProfileCreate):
    profile_in_db = db.query(models.Profile).filter(models.Profile.email == profile.email)
    if profile_in_db.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Profile with {profile.email} already exist")
    new_profile = models.Profile(**profile.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

def get_profile(db: Session,email: str):
    profile = db.query(models.Profile).filter(models.Profile.email == email)
    if profile.first():
        return profile.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Profile with {email} not found")

def update_profile(db: Session,email: str,profile: schemas.ProfileUpdate):
    profile_in_db = db.query(models.Profile).filter(models.Profile.email == email)
    if profile_in_db.first():
        profile_in_db.update(profile)
        db.commit()
        return {"message": "Profile updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Profile with {email} not found")

def delete_profile(db: Session,email: str):
    profile_in_db = db.query(models.Profile).filter(models.Profile.email == email)
    if profile_in_db.first():
        profile_in_db.delete()
        db.commit()
        return {"message": "Profile deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Profile with {email} not found")

