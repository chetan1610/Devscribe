
from app.models.follow import Follow
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

async def get_follow(db:AsyncSession,follower_id:int,following_id:int)->Follow|None:
    follow=await db.execute(select(Follow).where(Follow.follower_id==follower_id,Follow.following_id==following_id))
    return follow.scalar_one_or_none()



async def create(db:AsyncSession,follower_id:int,following_id:int):
    follow=Follow(follower_id=follower_id,
                  following_id=following_id)
    db.add(follow)
    await db.commit()
    await db.refresh(follow)
    return follow
    
async def delete(db,follow:Follow)->None:
    await db.delete(follow)
    await db.commit()
    


async def get_followers(db:AsyncSession,user_id:int)->list[User]:
    result=await db.execute(select(User)
                            .join(Follow,Follow.follower_id==User.id)
                            .where(Follow.following_id==user_id))
    return result.scalars().all()



async def get_following(db:AsyncSession,user_id:int)->list[User]:
    result= await db.execute(select(User)
                             .join(Follow,Follow.following_id==User.id)
                             .where(Follow.follower_id==user_id))
    
    return result.scalars().all()
