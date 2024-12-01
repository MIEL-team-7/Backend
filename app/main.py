import uvicorn

from fastapi import FastAPI

from sqladmin.authentication import AuthenticationBackend
from sqladmin import Admin, ModelView
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.core.db import engine
from app.models.models import Manager, Office, Candidate
from app.utils.admin_panel import AdminAuth, ManagerAdmin, OfficeAdmin, CandidateAdmin, CourseAdmin, CandidateCourseAdmin, ManagerCandidateAdmin

app = FastAPI()
authentication_backend = AdminAuth(secret_key="...")
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(ManagerAdmin)
admin.add_view(OfficeAdmin)
admin.add_view(CandidateAdmin)
admin.add_view(CourseAdmin)
admin.add_view(CandidateCourseAdmin)
admin.add_view(ManagerCandidateAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8188, reload=True)

