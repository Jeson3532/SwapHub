from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

CHAINLIT_AUTH_SECRET = os.getenv("CHAINLIT_AUTH_SECRET")
schema = OAuth2PasswordBearer(tokenUrl='/me')
algorithms = ['HS256']


def get_current_user(token: str = Depends(schema)):
    meta = jwt.decode(token, key=CHAINLIT_AUTH_SECRET, algorithms=algorithms)
    return meta
