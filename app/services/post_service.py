from app.schemas.post import PostCreate
from slugify import slugify
from app.repositories import post_repository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from app.models.post import Post
import json
from app.core.redis import redis_client
from app.schemas.post import PostOut

async def create_post(db:AsyncSession,author_id:int,data:PostCreate):
    slug=slugify(data.title)
    existing=await post_repository.get_by_slug(db,slug)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=" A post with this title already exists")
    keys=await redis_client.keys("feed:*")
    if keys:
        await redis_client.delete(*keys)
    
    return await post_repository.create(db,author_id,data.title,data.content,slug,data.status)
    
    
async def get_post(db:AsyncSession,slug:str)->Post:
    post=await post_repository.get_by_slug(db,slug)
    if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" A post with this title not exists")
        
    return post


async def get_feed(db:AsyncSession,user_id:int,limit:int=10,offset:int=0):
    cache_key=f"feed:{user_id}"
    
    cached=await redis_client.get(cache_key)
    if cached is not None:
        print(">>>CACHE HIT")
        return json.loads(cached)
    print(">>>CACHE MISS")
    posts= await post_repository.get_feed(db,user_id,limit,offset)
    posts_data=[PostOut.model_validate(p).model_dump(mode="json") for p in posts]
    print("stroing in redis")
    await redis_client.set(cache_key,json.dumps(posts_data),ex=60)
    print("stored")
    return posts_data