from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    published: Optional[bool] = False

#This is the model for the request which user sends to the server.
class Post(PostBase):
    content: str
    rating: Optional[int] = None


#This is the model for the response which user gets back from the server.
#In this project it is used only in "post/id"
class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode=True

############################################################################################

# User Schema

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    created_at: datetime
    id: int

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginToken(BaseModel):
    access_token: str
    token_type: str

# Schema for the Token Data i.e. the data embedded into Token.
class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode=True