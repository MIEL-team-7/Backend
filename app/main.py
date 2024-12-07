import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from app.core.db import engine
from app.core.logging import logger
from app.utils.admin_panel import (
    AdminAuth,
    ManagerAdmin,
    OfficeAdmin,
    CandidateAdmin,
    CourseAdmin,
    CandidateCourseAdmin,
    ManagerCandidateAdmin,
)
from app.utils.routers import register_routers

app = FastAPI()


authentication_backend = AdminAuth(secret_key="...")
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(ManagerAdmin)
admin.add_view(OfficeAdmin)
admin.add_view(CandidateAdmin)
admin.add_view(CourseAdmin)
admin.add_view(CandidateCourseAdmin)
admin.add_view(ManagerCandidateAdmin)

register_routers(app)

if __name__ == "__main__":
    logger.info("Запуск сервера...")
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
