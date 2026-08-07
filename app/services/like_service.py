from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import like_repository, post_repository


async def like_post(db: AsyncSession, user_id: int, post_id: int):
    post = await post_repository.get_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    existing = await like_repository.get_like(db, user_id, post_id)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already liked this post")
    return await like_repository.create(db, user_id, post_id)


async def unlike_post(db: AsyncSession, user_id: int, post_id: int) -> None:
    like = await like_repository.get_like(db, user_id, post_id)
    if like is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You haven't liked this post")
    await like_repository.delete(db, like)