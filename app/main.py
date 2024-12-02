import uvicorn

from fastapi import FastAPI

from app.utils.routers import register_routers
from app.core.logging import logger

app = FastAPI()

register_routers(app)

if __name__ == "__main__":
    logger.info("Запуск сервера...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
