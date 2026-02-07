import chainlit as cl
from dotenv import load_dotenv
from src.utils.prompt_extraction import get_prompt

from src.frontend.auth import callback
from src.frontend.handlers import messages
from src.frontend.ollama_client.client import get_async_client_llm
from src.utils.consts import AVAILABLE_MODELS

load_dotenv()
SYSTEM_PROMPT = get_prompt(prompt_name='llama3_prompt.yaml')
CURRENT_MODEL: AVAILABLE_MODELS = 'llama3'

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
    # Прогрев модели
    await get_async_client_llm().chat(
        model=CURRENT_MODEL,
        keep_alive="10m"
    )
    system_prompt = {"role": "system", "content": SYSTEM_PROMPT}
    cl.user_session.set("history", [system_prompt])



