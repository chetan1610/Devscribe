from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from app.repositories import post_repository,comment_repository






async def add_comment(db:AsyncSession,post_id:int,author_id,content:str):
    post=await post_repository.get_by_id(db,post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    return await comment_repository.create(db,post_id,author_id,content)


async def list_comments(db:AsyncSession,post_id:int)->list[Comment]:
    return await comment_repository.get_by_post(db,post_id)

async def delete_comment(db:AsyncSession,comment_id:int,user_id:int):
    comment=await comment_repository.get_by_id(db,comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="comment not found")
    if comment.author_id!=user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="the comment is not yours")
    await comment_repository.delete(db,comment)