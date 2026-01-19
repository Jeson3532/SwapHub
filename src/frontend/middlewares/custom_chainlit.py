import os
from functools import wraps
import chainlit as cl
from typing import Callable
from src.utils.log import logger
from src.utils import log_input_message
import time


def on_message(func: Callable):
    @wraps(func)
    async def wrapper(message: cl.Message):
        user = cl.user_session.get("user")
        await log_input_message(user, message)  # Логирование входящих сообщений
        result = await func(message)
        return result

    return cl.on_message(wrapper)
