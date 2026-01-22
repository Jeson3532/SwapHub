from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
import jwt
from jwt.exceptions import DecodeError
import os
from dotenv import load_dotenv
from src.utils import logger
from datetime import datetime, timedelta, timezone

load_dotenv()

CHAINLIT_AUTH_SECRET = os.getenv("CHAINLIT_AUTH_SECRET")
algorithms = ['HS256']

token_scheme = APIKeyCookie(name="access_token", auto_error=True)


def get_current_user(token: str = Depends(token_scheme)):
    try:
        meta = jwt.decode(token, key=CHAINLIT_AUTH_SECRET, algorithms=algorithms)
        return meta
    except DecodeError as e:
        logger.error(f"Ошибка декордирования: {e}")
        raise HTTPException(status_code=401, detail="Невалидный токен")
    except Exception as e:
        logger.error(f"Ошибка при авторизации: {e}")
        raise HTTPException(status_code=401, detail="Ошибка при авторизации")


def create_access_token(identifier, display_name, metadata: dict, time_minutes: int = 60):
    iat = datetime.now(tz=timezone.utc)
    payload = {
        'identifier': identifier,
        'display_name': display_name,
        'metadata': metadata,
        'exp': iat + timedelta(minutes=time_minutes),
        'iat': iat
    }
    return jwt.encode(payload, key=CHAINLIT_AUTH_SECRET, algorithm=algorithms[0])


