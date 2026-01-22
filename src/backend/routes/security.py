from fastapi import APIRouter, Body
from src.backend.models import auth as auth_m
from src.database.postgres.tables import Users
from src.database.postgres.methods import AuthMethods
from src.utils import security
from src.utils.enums import UserRole

router = APIRouter(prefix='/auth', tags=['Авторизация/Регистрация'])



### Далее - переделать, чтобы регистрировать сотрудников в системе мог только администратор
@router.post("/register", response_model=auth_m.UserRegResponse)
async def _(form: auth_m.UserRegForm = Body()):
    attr = {
        "username": form.username,
        "password": security.hash_password(form.password),
        "email": form.email,
        "role": UserRole.EMPLOYEE
    }
    user = Users(**attr)
    await AuthMethods.register_user(user)
    return auth_m.UserRegResponse.model_validate(attr)
