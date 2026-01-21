import os
import pyprojroot as ppr

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import uvicorn

from src.backend.middlewares.http import dispatch_host

from chainlit.utils import mount_chainlit
from src.backend.routes import all_routers
from src.utils import logger

root_path = ppr.here()
frontend_app_path = str(root_path.joinpath("src/frontend/app.py"))


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Backend запущен.")
    yield
    logger.info("Backend отключен.")


app = FastAPI(title="ChatLLMA 3.0 Swagger API", version="1.0.1", lifespan=lifespan)

# Импорт всех роутеров
for router in all_routers:
    app.include_router(router)
# Добавление middleware'ов
app.middleware("http")(dispatch_host)
# Подключение фронта
mount_chainlit(app=app, path="/assistant", target=frontend_app_path)

if __name__ == '__main__':
    uvicorn.run("src.backend.entry:app", host="localhost", port=8000, reload=True)
