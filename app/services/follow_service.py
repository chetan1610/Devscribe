from sqlalchemy.ext.asyncio import AsyncSession
from app.models.follow import Follow
from app.repositories import user_repository,follow_repository

from fastapi import HTTPException,status







async def follow_user(db:AsyncSession,follower_id:int,username:str)->Follow:
    target=await user_repository.get_by_username(db,username)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this user not found")
    
    if target.id==follower_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you cannot follow yourself")
    
    existing= await follow_repository.get_follow(db,follower_id,target.id)
    
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Already following this user")
    
    return await follow_repository.create(db,follower_id,target.id)



async def unfollow_user(db:AsyncSession,follower_id:int,username:str)->None:
    target=await user_repository.get_by_username(db,username)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this user not found")
    
    follow=await follow_repository.get_follow(db,follower_id,target.id)
    if follow is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you are not even following ")
    
    await follow_repository.delete(db,follow)