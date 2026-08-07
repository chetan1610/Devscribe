from fastapi import APIRouter,status
from app.core.database import get_db
from app.core.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.models.user import User
from app.services import follow_service
from app.repositories import user_repository,follow_repository
from app.schemas.user import UserOut
from app.repositories import user_repository,follow_repository
from fastapi import HTTPException,status

router=APIRouter(prefix="/users",tags=["follows"])


@router.post("/{username}/follow",status_code=status.HTTP_201_CREATED)
async def follow(username:str,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    await follow_service.follow_user(db,current_user.id,username)
    return {"detail":f"you rae now following{username}"}


@router.delete("/{username}/follow",status_code=status.HTTP_200_OK)
async def unfollow(username:str,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    await follow_service.unfollow_user(db,current_user.id,username)
    return {"detail":f"you unfollowed this {username}"}


@router.get("/{username}/followers",response_model=list[UserOut])
async def followers(username:str,db:AsyncSession=Depends(get_db)):
    user=await user_repository.get_by_username(db,username)
    if user is None:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail="User not found")
    return await follow_repository.get_followers(db,user.id)


@router.get("/{username}/following",response_model=list[UserOut])
async def following(username:str,db:AsyncSession=Depends(get_db)):
    user=await user_repository.get_by_username(db,username)
    if user is None:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail="User not found")
    return await follow_repository.get_following(db,user.id)



