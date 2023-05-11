from datetime import timedelta,datetime
from jose import JWTError,jwt
from config import SECRET_KEY
from typing import Annotated
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from db import DataBase
from models import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    
    
    def get_current_user(self, token: Annotated[str,Depends(oauth2_scheme)]):
        credential_expection = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Counld Not Validate Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

        try:
            payload = jwt.decode(token=token,key=SECRET_KEY,algorithms="HS256")
            username: str = payload.get("sub")
            if username is None:
                raise credential_expection
            token_data = TokenData(username=username)
        except JWTError:
            raise credential_expection
        user = DataBase.get_user(username=username)
        
        return {
            "status_code":user[0],
            "user": user
        }
    

        

    

    



    


        
