from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from sqlalchemy import select


async def create(db:AsyncSession,post_id:int,author_id:int,content:str)->Comment:
    comment=Comment(post_id=post_id,
                    author_id=author_id,
                    content=content)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

async def get_by_post(db:AsyncSession,post_id:int)->list[Comment]:
    result= await db.execute(select(Comment).where(Comment.post_id==post_id))
    return result.scalars().all()

async def get_by_id(db:AsyncSession,id:int)->Comment|None:
    result= await db.execute(select(Comment).where(Comment.id==id))
    return result.scalar_one_or_none()


async def delete(db:AsyncSession,comment:Comment)->None:
    await db.delete(comment)
    await db.commit()