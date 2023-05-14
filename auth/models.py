from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import hashing

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True,default=hashing.Hash.get_random_id())
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
