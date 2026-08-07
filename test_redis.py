import asyncio
from app.core.redis import redis_client


async def main():
    await redis_client.set("test", "hello")
    value = await redis_client.get("test")
    print("Redis says:", value)


asyncio.run(main())