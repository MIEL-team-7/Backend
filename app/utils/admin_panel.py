from sqladmin.authentication import AuthenticationBackend
from sqladmin import ModelView
from starlette.requests import Request
from app.models.models import (
    Manager,
    Office,
    Candidate,
    Course,
    CandidateCourse,
    ManagerCandidate,
)
from app.utils.authentication import get_password_hash


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        print(type(form))
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

    name = "Руководитель"
    name_plural = "Руководители"

    async def on_model_change(self, data: dict, model: Manager, is_created: bool, request: Request) -> None:
        if is_created:
            data["password"] = get_password_hash(data["password"])

    column_list = [Manager.full_name, Manager.email, Manager.office, Manager.quotas]

    

    form_columns = [
        Manager.full_name,
        Manager.email,
        Manager.password,
        Manager.quotas,
        Manager.office,
        Manager.candidates,
    ]
    column_searchable_list = [
        Manager.full_name,
        Manager.email,
        Manager.quotas,
        Manager.office,
    ]
    column_sortable_list = [Manager.full_name, Manager.email, Manager.quotas]

    column_labels = {
        Manager.full_name: "ФИО",
        Manager.email: "Электронная почта",
        Manager.office: "Офис",
        Manager.quotas: "Количество квот",
        Manager.password: "Пароль",
        Manager.candidates: "Кандидаты"
    }

    
class OfficeAdmin(ModelView, model=Office):
    name = "Офис"
    name_plural = "Офисы"

    column_list = [Office.id, Office.name, Office.location, Office.managers]
    column_searchable_list = [Office.id, Office.name, Office.location]
    column_sortable_list = [Office.id, Office.name, Office.location]
    form_columns = [Office.name, Office.location, Office.managers]
    column_labels = {
        Office.name: "Название",
        Office.location: "Локация",
        Office.managers: "Руководитель"
    }

class CandidateAdmin(ModelView, model=Candidate):
    name = "Кандидат"
    name_plural = "Кандидаты"

    column_list = [
        Candidate.id,
        Candidate.full_name,
        Candidate.email,
        Candidate.location,
        Candidate.phone,
        Candidate.is_hired,
        Candidate.clients,
        Candidate.objects,
        Candidate.courses,
    ]
    column_searchable_list = [
        Candidate.id,
        Candidate.full_name,
        Candidate.email,
        Candidate.location,
        Candidate.objects,
    ]
    column_sortable_list = [
        Candidate.id,
        Candidate.full_name,
        Candidate.email,
        Candidate.location,
        Candidate.phone,
        Candidate.is_hired,
        Candidate.clients,
        Candidate.objects,
    ]
    form_columns = [
        Candidate.full_name,
        Candidate.email,
        Candidate.location,
        Candidate.phone,
        Candidate.is_hired,
        Candidate.clients,
        Candidate.objects,
    ]

    column_labels = {
        Candidate.full_name: "ФИО",
        Candidate.email: "Электронная почта",
        Candidate.location: "Адрес",
        Candidate.phone: "Телефон",
        Candidate.is_hired: "Приглашен",
        Candidate.clients: "Клиенты",
        Candidate.objects: "Объекты",
        Candidate.courses: "Курсы",
    }


class CourseAdmin(ModelView, model=Course):
    name = "Курс"
    name_plural = "Курсы"

    column_list = [Course.id, Course.name, Course.candidates]
    column_searchable_list = [Course.id, Course.name, Course.candidates]
    form_columns = [Course.name]
    column_labels = {
        Course.name: "Название",
        Course.candidates: "Кандидаты"
    }

class CandidateCourseAdmin(ModelView, model=CandidateCourse):
    name = "Кандидат-курс"
    name_plural = "Кандидаты-курсы"

    column_list = [
        CandidateCourse.id,
        CandidateCourse.candidate,
        CandidateCourse.course,
    ]
    column_searchable_list = [CandidateCourse.id]
    column_sortable_list = [CandidateCourse.id]
    form_columns = [CandidateCourse.candidate, CandidateCourse.course]

    column_labels = {
        CandidateCourse.candidate: "Кандидат",
        CandidateCourse.course: "Курс",
    }

    column_labels = {
        CandidateCourse.candidate: "Кандидат",
        CandidateCourse.course: "Курс"
    }

class ManagerCandidateAdmin(ModelView, model=ManagerCandidate):
    name = "История приглашений"
    name_plural = "История приглашений"

    def get_created_at(self, obj):
        my_date = self.created_at
        formatted_date = my_date.strftime("%Y-%m-%d %H:%M")
        return formatted_date

    def get_updated_at(self, obj):
        my_date = self.updated_at
        formatted_date = my_date.strftime("%Y-%m-%d %H:%M")
        return formatted_date

    column_list = [
        ManagerCandidate.id,
        ManagerCandidate.manager,
        ManagerCandidate.candidate,
        ManagerCandidate.created_at,
        ManagerCandidate.updated_at,
        ManagerCandidate.is_viewed,
    ]
    column_searchable_list = [
        ManagerCandidate.id,
        ManagerCandidate.created_at,
        ManagerCandidate.updated_at,
        ManagerCandidate.is_viewed,
    ]
    column_sortable_list = [
        ManagerCandidate.id,
        ManagerCandidate.created_at,
        ManagerCandidate.updated_at,
        ManagerCandidate.is_viewed,
    ]
    form_columns = [ManagerCandidate.manager, ManagerCandidate.candidate]

    column_labels = {
        ManagerCandidate.manager: "Руководитель",
        ManagerCandidate.candidate: "Кандидат",
        ManagerCandidate.is_viewed: "Приглашен",
        ManagerCandidate.created_at: "Время создания",
        ManagerCandidate.updated_at: "Время редактирования",
    }

    column_formatters = {
        ManagerCandidate.created_at: get_created_at,
        ManagerCandidate.updated_at: get_updated_at,
    }
