import chainlit as cl
from src.database.postgres.methods import AuthMethods as auth_m
from src.utils.security import verify_password
from src.utils import logger
from src.utils.enums import UserRole


@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    user = await auth_m.get_user(username)
    if not user:
        return None
    payload = {
        'identifier': username,
        'metadata': {
            'role': UserRole(user.role).value,
            'experience': user.experience,
            'department': user.department,
            'email': user.email
        }
    }
    verify = verify_password(password, hash_pass=user.password)
    if verify:
        return cl.User(**payload)
    else:
        return cl.ErrorMessage(content="Не удалось войти.")
