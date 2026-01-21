import chainlit as cl
from dotenv import load_dotenv
from src.utils.prompt_extraction import get_prompt

from src.frontend.auth import callback
from src.frontend.handlers import messages


load_dotenv()
SYSTEM_PROMPT = get_prompt(prompt_name='llama3_prompt.yaml')


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



