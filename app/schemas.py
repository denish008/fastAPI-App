from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint
from typing import Optional

class User(BaseModel):
    email : EmailStr
    password : str
    id : int
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

#----------------------------------------------------------------------------------------------------------#

class PostBase(BaseModel):
    title : str
    content : str
    published : Optional[bool] = True
    class Config:
        from_attributes = True   

class Post(PostBase):
    owner_id : int
    created_at : datetime
    id : int
    owner : User
#----------------------------------------------------------------------------------------------------------#

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None 
#----------------------------------------------------------------------------------------------------------#

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)