from app.routers.manager_router import manager_router
from app.routers.auth_router import auth_router


def register_routers(app):
    app.include_router(manager_router)
    app.include_router(auth_router)
