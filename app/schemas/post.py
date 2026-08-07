from datetime import datetime

from pydantic import BaseModel,EmailStr


class PostCreate(BaseModel):
    title:str
    content:str
    status:str="draft"
    
    
class AuthorOut(BaseModel):
    id:int
    username:str
    model_config={"from_attributes":True}

    
class PostOut(BaseModel):
    id:int
    title:str
    content:str
    slug:str
    author_id:int
    status:str
    author:AuthorOut
    created_at:datetime
    model_config={"from_attributes":True}