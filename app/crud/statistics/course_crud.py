from fastapi.params import Depends
from sqlalchemy import func, column
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
    courses = result.scalars().unique().all()
    for course in courses:
        course.candidates_count = await read_candidates_count_by_course_id(course.id, session)
    return courses


async def get_candidates_count_by_course_id(course_id: int, session: AsyncSession = Depends(get_session)):
    """Получение количества кандидатов по id курса"""
    request = select(func.count()).select_from(Candidate).join(CandidateCourse).filter(CandidateCourse.course_id == course_id)
    result = await session.execute(request)
    candidates_count = result.scalar_one()
    return candidates_count
