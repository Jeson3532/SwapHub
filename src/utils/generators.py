import secrets
import string

dictionary = string.ascii_letters + string.digits


def generate_message_id(length: int = 8):
    return ''.join(secrets.choice(dictionary) for _ in range(length))

