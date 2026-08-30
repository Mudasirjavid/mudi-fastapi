
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class config:
        orm_mode=True
        

class Post(BaseModel):
    title:str 
    content:str
    published:bool=True
   
    
class CreatePost(Post):
   pass

class Posts(Post):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    class config:
        orm_mode=True
        
class PostOut(BaseModel):
    Post: Posts  
    Likes: int

    class Config:
        from_attributes = True 
 
    
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    

        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id: int
    dir:int=Field(le=1)