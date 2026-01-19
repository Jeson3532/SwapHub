import logging
from fastapi import Request
import jwt
from dotenv import load_dotenv
import os
from src.database.redis import get_redis_client
from datetime import datetime
import chainlit as cl
from typing import Union
import redis as r
from .id_generator import generate_message_id
import aiofiles

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

load_dotenv()

CHAINLIT_AUTH_SECRET = os.getenv("CHAINLIT_AUTH_SECRET")
STATIC_LOG_DESIGN = "LEVEL  | LOG_TYPE  |   CURRENT_TIME    |   IP-ADDRESS  |   COMMENT"  # Design - Designations
algorithms = ['HS256']


async def log_entrance(request: Request):
    auth_token = request.cookies.get("access_token")
    if auth_token:
        try:
            address = request.client.host

            payload = jwt.decode(auth_token, key=CHAINLIT_AUTH_SECRET, algorithms=algorithms)
            ident = payload.get("identifier", None)
            if ident:
                template = f"{ident}_address"

                async with get_redis_client() as client:
                    success_created = await client.set(template, address, ex=900, nx=True)
                    if success_created:
                        msg = f"Вход в систему с идентификатором '{ident}'"
                        logger.info(msg)
                        await add_info(msg, level='INFO', log_type="USER_ENTRANCE", ip_address=address)

        except jwt.exceptions.PyJWTError as e:
            logger.debug(e)
        except Exception as e:
            logger.error(e)


async def log_input_message(user: cl.User, message: cl.Message):
    try:
        identifier = user.identifier
        if identifier:
            template = f"{identifier}_address"
            async with get_redis_client() as client:
                address = await client.get(template)
                message_id = generate_message_id()
                success_created = await client.set(f"{identifier}_message_id", message_id, nx=True, ex=30)
                if success_created:
                    msg = f"[{message_id}] Сообщение от пользователя '{identifier}': {message.content}"

                    logger.info(msg)
                    await add_info(msg, level="INFO", log_type="MESSAGE_FROM_USER", ip_address=address)
    except r.exceptions.RedisError as e:
        logger.error(e)


async def log_output_message(user: cl.User, message: cl.Message, time_answer: float):
    try:
        identifier = user.identifier
        if identifier:
            template = f"{identifier}_address"
            async with get_redis_client() as client:
                address = await client.get(template)
                message_id = await client.get(f"{identifier}_message_id")
                if not message_id:
                    message_id = "Unknown"
                msg = f"[{message_id}] Ответ модели для '{identifier}': {message.content} (Ответ занял {time_answer}s)"

                await client.delete(f"{identifier}_message_id")

            logger.info(msg)
            await add_info(msg, level="INFO", log_type="MESSAGE_FROM_MODEL", ip_address=address)
    except r.exceptions.RedisError as e:
        logger.error(e)


async def add_info(information: str,
                   log_type: str,
                   encoding: str = 'utf-8',
                   path_dir='src/files',
                   ip_address: Union[str, None] = None,
                   level: str = "INFO"
                   ):
    logfile_name = datetime.now().strftime("%d-%m-%Y") + ".log"
    full_path = os.path.join(path_dir, logfile_name)
    current_time = datetime.now().strftime("%H:%M:%S:%f")[:-2]

    os.makedirs(path_dir, exist_ok=True)
    file_exists = os.path.exists(full_path)
    try:
        async with aiofiles.open(full_path, "a", encoding=encoding) as f:
            if not file_exists:
                await f.write(STATIC_LOG_DESIGN + '\n')
            await f.write(f"{level}   |   {log_type}  |   {current_time}    |   {ip_address}  |   {information}\n")
    except PermissionError as e:
        logger.error(f'Ошибка на уровне прав: {e}')
    except OSError as e:
        logger.error(f'Ошибка на уровне OS: {e}')
