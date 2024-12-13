from app.routers.manager_router import manager_router

def register_routers(app):
    app.include_router(manager_router)
