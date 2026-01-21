from fastapi import APIRouter, Depends
from src.backend.auth.oauth import get_current_user

router = APIRouter(prefix='/testing')


@router.get("/me")
async def _(user=Depends(get_current_user)):
    return user
