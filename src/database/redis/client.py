from redis.asyncio import Redis, ConnectionPool
import platform
import os

REDIS_HOST = "localhost" if platform.system() == "Windows" else os.getenv("REDIS_HOST")

pool = ConnectionPool(
    host=REDIS_HOST,
    port=6379,
    db=0,
    decode_responses=True
)


def get_redis_client() -> Redis:
    return Redis(connection_pool=pool)
