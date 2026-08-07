from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.like import Like


async def get_like(db: AsyncSession, user_id: int, post_id: int) -> Like | None:
    result = await db.execute(select(Like).where(Like.user_id == user_id, Like.post_id == post_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, user_id: int, post_id: int) -> Like:
    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    await db.commit()
    await db.refresh(like)
    return like


async def delete(db: AsyncSession, like: Like) -> None:
    await db.delete(like)
    await db.commit()


async def count_likes(db: AsyncSession, post_id: int) -> int:
    result = await db.execute(select(func.count()).where(Like.post_id == post_id))
    return result.scalar()