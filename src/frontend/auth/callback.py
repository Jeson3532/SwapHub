import chainlit as cl


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "experience": "293", "department": "Отдел IT-инфраструктуры"}
        )
    else:
        return None
