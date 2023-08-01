from sqlalchemy import Boolean, Column, Integer, String
from ..utils import hashing
from .database import Base
import secrets


class User(Base):
    """
        User class for authentcation
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True,default=secrets.token_hex(16))
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
