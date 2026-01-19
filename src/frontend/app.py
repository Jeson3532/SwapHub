import chainlit as cl
import ollama
from functools import lru_cache
from dotenv import load_dotenv
import os
import platform
import src.frontend.middlewares.custom_chainlit as ccl
from src.utils import log_output_message
import time

load_dotenv()
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
OLLAMA_HOST = "localhost:11434" if platform.system() == "Windows" else os.getenv("OLLAMA_HOST")


@lru_cache
def get_async_client_llm():
    return ollama.AsyncClient(host=OLLAMA_HOST)


@cl.on_chat_start
async def startup():
    global SYSTEM_PROMPT
    # Информация о пользователе
    user = cl.user_session.get("user")
    user_meta = user.metadata
    # Внесение информации в промт
    SYSTEM_PROMPT = SYSTEM_PROMPT.format(
        role=user_meta.get("role", None),
        department=user_meta.get("department", None),
        experience=user_meta.get("experience", None)
    )
    system_prompt = {"role": "system", "content": SYSTEM_PROMPT}
    cl.user_session.set("history", [system_prompt])


@ccl.on_message
async def message_handler(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({'role': "user", 'content': message.content})

    msg = cl.Message(content="")
    stream = await get_async_client_llm().chat(
        model='llama3',
        stream=True,
        messages=history
    )
    start_time = time.time()
    async for chunk in stream:
        content = chunk.message.content
        if content:
            await msg.stream_token(content)
    end_time = time.time()

    time_answer_model = round(end_time - start_time, 2)  # Время ответа модели без учета стриминга
    history.append({'role': 'assistant', 'content': msg.content})
    cl.user_session.set("history", history)

    await log_output_message(cl.user_session.get("user"), msg,
                             time_answer=time_answer_model)  # Логирование сообщения от модели
    await msg.send()


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "experience": "293", "department": "Отдел IT-инфраструктуры"}
        )
    else:
        return None
