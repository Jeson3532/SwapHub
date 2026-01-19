import os
import pyprojroot as ppr

from fastapi import FastAPI, Request
import uvicorn

from src.backend.routes.log import router as log_router
from src.backend.middlewares.http import dispatch_host

from chainlit.utils import mount_chainlit

root_path = ppr.here()
frontend_app_path = str(root_path.joinpath("src/frontend/app.py"))

app = FastAPI(title="ChatLLMA 3.0 Swagger API", version="1.0.1")
app.include_router(log_router)
app.middleware("http")(dispatch_host)

mount_chainlit(app=app, path="/assistant", target=frontend_app_path)
if __name__ == '__main__':
    uvicorn.run("src.backend.entry:app", host="localhost", port=8000, reload=True)
