from fastapi import APIRouter, Request
import logging

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

router = APIRouter()

# @router.get("/assistant")
# async def _(request: Request):
#     print("DA")
#     print(f"IP-address: {request.client.host}")