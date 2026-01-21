from fastapi import APIRouter, Request


router = APIRouter(tags=['Администрирование'])


@router.get("/check-my-ip", description="Показывает реальный IP, если проект запущен на Unix-системе.")
async def check_ip(request: Request):
    return {
        "client_host": request.client.host,
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
        "x_real_ip": request.headers.get("x-real-ip")
    }
