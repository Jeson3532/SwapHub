from pwdlib import PasswordHash

pwd = PasswordHash.recommended()


def hash_password(password: str):
    return pwd.hash(password)


def verify_password(password: str, hash_pass: str):
    return pwd.verify(password, hash_pass)



