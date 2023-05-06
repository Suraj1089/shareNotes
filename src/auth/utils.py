from db import client
from datetime import timedelta,datetime
from jose import JWTError,jwt
from config import SECRET_KEY

class Auth:
    """
        class for handling user authentication
    """
    def __init__(self) -> None:
        pass 

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({'expire':expire})
        return jwt.encode(to_encode,SECRET_KEY,algorithm="HS256")
    
    
    



    


        
