from fastapi import APIRouter, Request, Depends
from src.backend.auth.oauth import get_current_user

router = APIRouter(tags=['Администрирование'])


@router.get("/check-my-ip", description="Показывает реальный IP, если проект запущен на Unix-системе.")
async def check_ip(request: Request, user=Depends(get_current_user)):
    return {
        "client_host": request.client.host,
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
        "x_real_ip": request.headers.get("x-real-ip")
    }
