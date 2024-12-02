from app.routers.manager_router import manager_router
from app.routers.statistics_router import statistics_router


def register_routers(app):
    app.include_router(manager_router)
    app.include_router(statistics_router)
