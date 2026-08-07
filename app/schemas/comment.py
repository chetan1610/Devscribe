from pydantic import BaseModel
from datetime import datetime



class CommentCreate(BaseModel):
    content:str
    
    
class CommentOut(BaseModel):
    id:int
    post_id:int
    author_id:int
    content:str
    created_at:datetime
    model_config={"from_attributes":True}