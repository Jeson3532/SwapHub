from src.frontend.middlewares import custom_chainlit as ccl
import chainlit as cl
from src.frontend.ollama_client.client import get_async_client_llm
from src.utils import log_output_message, logger
from src.utils.consts import METRICS_OLLAMA_MODEL, AVAILABLE_MODELS
from src.frontend.app import CURRENT_MODEL


@ccl.on_message
async def message_handler(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({'role': "user", 'content': message.content})
    msg = cl.Message(content="")
    stream = await get_async_client_llm().chat(
        model=CURRENT_MODEL,
        stream=True,
        messages=history
    )
    done_token_meta = dict()
    async for chunk in stream:
        content = chunk.message.content
        if content:
            await msg.stream_token(content)
        if chunk.get("done"):
            done_token_meta = {k: v for k, v in chunk.model_dump().items() if k in METRICS_OLLAMA_MODEL}

    history.append({'role': 'assistant', 'content': msg.content})
    cl.user_session.set("history", history)
    await log_output_message(cl.user_session.get("user"), msg,
                             ollama_meta=done_token_meta)  # Логирование сообщения от модели
    await msg.send()
