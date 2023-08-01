from pydantic import BaseModel,EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str
    password: str

class UserDelete(BaseModel):
    email: str

class UserList(BaseModel):
    email: str
    name: str


class Profile(BaseModel):
    email: str
    name: str
    password: str

    class Config:
        orm_mode = True

class ProfileCreate(BaseModel):
    email: str
    name: str
    password: str

class ProfileUpdate(BaseModel):
    email: str
    name: str
    password: str

class ProfileDelete(BaseModel):
    email: str

class ProfileList(BaseModel):
    email: str
    name: str
    password: str

    