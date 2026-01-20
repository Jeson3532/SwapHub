import logging
from fastapi import Request
import jwt
from dotenv import load_dotenv
import os
from datetime import datetime
import chainlit as cl
from typing import Union
import redis as r
from src.utils.enums import LogTypes
import aiofiles
from src.database.redis import methods as r_methods

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

load_dotenv()

CHAINLIT_AUTH_SECRET = os.getenv("CHAINLIT_AUTH_SECRET")
STATIC_LOG_DESIGN = "LEVEL  | LOG_TYPE  |   CURRENT_TIME    |   IP-ADDRESS  |   COMMENT"  # Design - Designations
algorithms = ['HS256']


async def log_entrance(request: Request):
    log_type = LogTypes.USER_ENTRANCE

    auth_token = request.cookies.get("access_token")
    if auth_token:
        try:
            address = request.client.host

            payload = jwt.decode(auth_token, key=CHAINLIT_AUTH_SECRET, algorithms=algorithms)
            ident = payload.get("identifier", None)
            result = await r_methods.set_address(ident, address)
            if result:
                msg = f"Вход в систему с идентификатором '{ident}'"
                logger.info(msg)
                await add_log_info(msg, level='INFO', log_type=log_type, ip_address=address)

        except jwt.exceptions.PyJWTError as e:
            logger.debug(e)
        except Exception as e:
            logger.error(e)


async def log_input_message(user: cl.User, message: cl.Message):
    log_type = LogTypes.MESSAGE_FROM_USER
    try:
        identifier = user.identifier
        if identifier:
            address = await r_methods.get_address(identifier)

            result = await r_methods.set_message_id(identifier)
            if result:
                msg = f"[{result['message_id']}] Сообщение от пользователя '{identifier}': {message.content}"

                logger.info(msg)
                await add_log_info(msg, level="INFO", log_type=log_type, ip_address=address)
            else:
                logger.debug(f"Возникла проблема при попытке логировать событие {log_type}.")
        else:
            logger.warning(f"Попытка логирования события {log_type} без идентификатора.")
    except r.exceptions.RedisError as e:
        logger.error(e)


async def log_output_message(user: cl.User, message: cl.Message, time_answer: float):
    log_type = LogTypes.MESSAGE_FROM_MODEL
    try:
        identifier = user.identifier
        if identifier:

            address = await r_methods.get_address(identifier)
            message_id = await r_methods.get_message_id(identifier)
            if not message_id:
                message_id = "Unknown"
            msg = f"[{message_id}] Ответ модели для '{identifier}': {message.content} (Ответ занял {time_answer}s)"
            logger.info(msg)
            await add_log_info(msg, level="INFO", log_type=log_type, ip_address=address)

            await r_methods.delete_message_id(identifier)
        else:
            logger.warning(f"Попытка логирования события {log_type} без идентификатора.")

    except r.exceptions.RedisError as e:
        logger.error(e)


async def add_log_info(information: str,
                       log_type: LogTypes,
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
            await f.write(f"{level}   |   {log_type.value}  |   {current_time}    |   {ip_address}  |   {information}\n")
    except PermissionError as e:
        logger.error(f'Ошибка на уровне прав: {e}')
    except OSError as e:
        logger.error(f'Ошибка на уровне OS: {e}')
