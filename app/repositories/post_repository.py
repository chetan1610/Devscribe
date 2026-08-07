from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.models.follow import Follow
from sqlalchemy.orm import selectinload

async def get_by_slug(db:AsyncSession,slug:str)->Post|None:
    result= await db.execute(select(Post).where(Post.slug==slug))
    return result.scalar_one_or_none()

async def get_by_id(db:AsyncSession,post_id:int)->Post|None:
    result=await db.execute(select(Post).where(Post.id==post_id))
    return result.scalar_one_or_none()



async def list_posts(db:AsyncSession,limit:int=10,offset:int=0)->list[Post]:
    result=await db.execute(
        select(Post)
        .where(Post.status=="published")
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def create(db:AsyncSession,author_id:int,title:str,content:str,slug:str,status:str)->Post:
    post=Post(author_id=author_id,
              title=title,
              content=content,slug=slug,
              status=status)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_feed(db:AsyncSession,user_id:int,limit:int=10,offset:int=0):
    result=await db.execute(select(Post)
                            .join(Follow,Follow.following_id==Post.author_id)
                            .where(Follow.follower_id==user_id,Post.status=="published")
                            .options(selectinload(Post.author))
                            .order_by(Post.created_at.desc())
                            .offset(offset)
                            .limit(limit))
    return result.scalars().all()
    

