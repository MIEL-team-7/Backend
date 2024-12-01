from typing import Annotated
import uvicorn
from sqladmin.authentication import AuthenticationBackend
from sqladmin import Admin, ModelView
from sqlalchemy.orm import joinedload
from starlette.requests import Request
from app.models.models import Manager, Office, Candidate, Course, CandidateCourse, ManagerCandidate


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


class ManagerAdmin(ModelView, model=Manager):
    column_list = [Manager.full_name, Manager.email, Manager.office, Manager.candidates, Manager.quotas]
    form_columns = [Manager.full_name, Manager.email, Manager.password, Manager.quotas, Manager.office, Manager.candidates]
    column_searchable_list = [Manager.full_name, Manager.email, Manager.quotas, Manager.office]
    column_sortable_list = [Manager.full_name, Manager.email, Manager.quotas]


class OfficeAdmin(ModelView, model=Office):
    column_list = [Office.id, Office.name, Office.location, 'managers_names']
    column_searchable_list = [Office.id, Office.name, Office.location]
    column_sortable_list = [Office.id, Office.name, Office.location]


class CandidateAdmin(ModelView, model=Candidate):
    column_list = [Candidate.id, Candidate.full_name, Candidate.email, Candidate.location, Candidate.phone, Candidate.is_hired, Candidate.clients, Candidate.objects, Candidate.managers]
    column_searchable_list = [Candidate.id, Candidate.full_name, Candidate.email, Candidate.location, Candidate.objects]
    column_sortable_list = [Candidate.id, Candidate.full_name, Candidate.email, Candidate.location, Candidate.phone, Candidate.is_hired, Candidate.clients, Candidate.objects]


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.name, Course.candidates]
    column_searchable_list = [Course.id, Course.name, Course.candidates]


class CandidateCourseAdmin(ModelView, model=CandidateCourse):
    column_list = [CandidateCourse.id, CandidateCourse.candidate, CandidateCourse.course]
    column_searchable_list = [CandidateCourse.id, CandidateCourse.candidate, CandidateCourse.course]


class ManagerCandidateAdmin(ModelView, model=ManagerCandidate):
    column_list =  [ManagerCandidate.id, ManagerCandidate.manager, ManagerCandidate.candidate, ManagerCandidate.is_viewed]
    column_searchable_list = [ManagerCandidate.id, ManagerCandidate.candidate, ManagerCandidate.is_viewed]
    column_sortable_list = [ManagerCandidate.id, ManagerCandidate.is_viewed]
