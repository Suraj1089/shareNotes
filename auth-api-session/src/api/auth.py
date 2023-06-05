
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status,Response
from .schemas import Token, User, UserInDB
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from .oauth import get_user,get_current_user,create_user,authenticate,create_access_token
from .config import ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY


auth = APIRouter()



@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: User):
    user_ = await get_user(user.email)
    print('users are', user_)
    if user_ is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with email {user.email} already exists!'
        )
    print('user created')
    return await create_user(user.dict())


@app.post("/token",response_model=Token,status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],response:Response):
    user = await authenticate(form_data.username,form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user.username},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(key="access_token",value=f"Bearer {token}", httponly=True) 
    return {"access_token": token, "token_type": "bearer"}




@app.get("/getUserData", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user