from src.frontend.middlewares import custom_chainlit as ccl
import chainlit as cl
from src.frontend.ollama_client.client import get_async_client_llm
import time
from src.utils import log_output_message

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
