from sqlalchemy import Boolean, Column, Integer, String
from . import hashing
from .database import Base


class User(Base):
    """
        User class for authentcation
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True,default=hashing.Hash.get_random_id())
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
