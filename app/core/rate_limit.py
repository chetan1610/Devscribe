from fastapi import HTTPException, status
from app.core.redis import redis_client


async def check_rate_limit(key: str, limit: int, window: int) -> None:
    current = await redis_client.incr(key)     
    if current == 1:
        await redis_client.expire(key, window)  
    if current > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )