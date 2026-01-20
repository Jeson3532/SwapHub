from src.database.redis.client import get_redis_client
from src.utils.generators import generate_message_id
from typing import Annotated, Any, Union
from redis.exceptions import RedisError
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')


async def set_address(identifier: str, address: str, exp: Annotated[int, "Время жизни в кеше (в секундах)"] = 60) -> \
        Union[
            dict, None]:
    try:
        template = f"{identifier}_address"

        async with get_redis_client() as client:
            success_created = await client.set(template, address, ex=exp, nx=True)
        return success_created
    except RedisError as e:
        logger.error(f"Ошибка с Redis: {e}")


async def set_message_id(identifier: str, exp: Annotated[int, "Время жизни в кеше (в секундах)"] = 60) -> Union[
    dict, None]:
    try:
        async with get_redis_client() as client:
            message_id = generate_message_id()
            success_created = await client.set(f"{identifier}_message_id", message_id, nx=True, ex=exp)
            if success_created is None:
                success_created = False
            return {"success_created": success_created, "message_id": message_id}
    except RedisError as e:
        logger.error(f"Ошибка с Redis: {e}")


async def get_address(identifier: str) -> Union[str, None]:
    try:
        template = f"{identifier}_address"
        async with get_redis_client() as client:
            address = await client.get(template)
            return address
    except RedisError as e:
        logger.error(f"Ошибка с Redis: {e}")


async def get_message_id(identifier: str) -> Union[str, None]:
    try:
        template = f"{identifier}_message_id"
        async with get_redis_client() as client:
            message_id = await client.get(template)
            return message_id
    except RedisError as e:
        logger.error(f"Ошибка с Redis: {e}")


async def delete_message_id(identifier: str) -> Union[int, None]:
    try:
        template = f"{identifier}_message_id"
        async with get_redis_client() as client:
            status = await client.delete(template)
            return status
    except RedisError as e:
        logger.error(f"Ошибка с Redis: {e}")
