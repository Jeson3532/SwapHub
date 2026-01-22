from fastapi import APIRouter, Depends
from src.backend.auth.oauth import get_current_user
from fastapi.security import APIKeyCookie
from src.backend.models.auth import UserDecodeTokenResponse

router = APIRouter(prefix='/testing', tags=["Тестирование"])


@router.get("/me", response_model=UserDecodeTokenResponse)
async def _(user: dict = Depends(get_current_user)):
    return user
