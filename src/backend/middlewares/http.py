from fastapi import Request
from src.utils import log_entrance


async def dispatch_host(request: Request, call_next):
    url = request.url.path
    if url.startswith("/assistant"):
        await log_entrance(request)

    response = await call_next(request)
    return response
