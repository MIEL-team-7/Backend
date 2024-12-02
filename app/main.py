import uvicorn

from fastapi import FastAPI

from app.utils.routers import register_routers


app = FastAPI()

register_routers(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
