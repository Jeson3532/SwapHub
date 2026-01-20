from fastapi import APIRouter, Request
import logging

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/check-ip")
async def check_ip(request: Request):
    print("HEADERS", request.headers)
    return {
        "client_host": request.client.host,
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
        "x_real_ip": request.headers.get("x-real-ip")
    }