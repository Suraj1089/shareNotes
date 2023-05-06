from passlib.context import CryptContext
from typing import Any


class Hash:
    """
        Utility class for Hashing passwords
    """
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self,plain_password: str,hashed_password: str):
        return self.pwd_context.verify(plain_password,hashed_password)
    
    
    def get_password_hash(self,plain_password: str):
        return self.pwd_context.hash(plain_password)
    
    


