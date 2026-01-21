from functools import lru_cache
import ollama
import platform
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = "localhost:11434" if platform.system() == "Windows" else os.getenv("OLLAMA_HOST")


@lru_cache
def get_async_client_llm():
    return ollama.AsyncClient(host=OLLAMA_HOST)
