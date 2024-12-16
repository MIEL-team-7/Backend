from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timedelta

from app.crud.statistics.candidate_crud import read_candidates_count_by_course_id
from app.models.models import Candidate, Manager, Course, CandidateCourse
from app.utils.database.test_data import get_session


async def read_course_by_id(course_id: int, session: AsyncSession = Depends(get_session)):
    course = await session.get(Course, course_id)
    if course:
        return course
    return None


async def read_courses(session: AsyncSession = Depends(get_session)):
    """Получение списка курсов с количеством кандидатов на них"""
    request = select(Course)
    result = await session.execute(request)
    courses = result.scalars().all()
    for course in courses:
        course.candidates_count = await read_candidates_count_by_course_id(course.id, session)
    return courses
