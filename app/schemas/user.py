from datetime import datetime

from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    username:str
    password:str
    
    
class UserOut(BaseModel):
    id:int
    username:str
    email:EmailStr
    bio:str|None
    created_at:datetime
    model_config={"from_attributes":True}
    
    
class TokenOut(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str="bearer"
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str