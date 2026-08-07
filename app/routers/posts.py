from fastapi import APIRouter,Depends,status,HTTPException
from app.schemas.post import PostOut,PostCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services import post_service








router=APIRouter(prefix="/posts",tags=["posts"])

@router.post("",response_model=PostOut,status_code=status.HTTP_201_CREATED)
async def create_post(data:PostCreate,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    return await post_service.create_post(db,current_user.id,data)




@router.get("/feed",response_model=list[PostOut])
async def feed(limit:int=10,offset:int=0,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    return await post_service.get_feed(db,current_user.id,limit,offset)



@router.get("/{slug}",response_model=PostOut)
async def get_post(slug:str,db:AsyncSession=Depends(get_db)):
    return await post_service.get_post(db,slug)
    