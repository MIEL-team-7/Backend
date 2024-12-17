from app.routers.manager_router import manager_router
from app.routers.auth_router import auth_router
from app.routers.invitation_router import invitation_of_manager
from app.routers.statistics_router import statistics_router


def register_routers(app):
    app.include_router(manager_router)
    app.include_router(auth_router)
    app.include_router(invitation_of_manager)
    app.include_router(statistics_router)
