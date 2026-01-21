from src.backend.routes.admin import router as admin_router
from src.backend.routes.security import router as security_router
from src.backend.routes.testing import router as testing_router
from fastapi import APIRouter

all_routers = list()

for key, val in dict(globals()).items():
    key_cond = '_router' in key
    val_cond = type(val) is APIRouter
    if key_cond and val_cond:
        all_routers.append(val)