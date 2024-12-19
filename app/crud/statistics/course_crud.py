from fastapi.params import Depends
from sqlalchemy import func, column
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timedelta

from app.crud.statistics.candidate_crud import read_candidates_count_by_course_id
from app.models.models import Candidate, Manager, Course, CandidateCourse
from app.utils.database.test_data import get_session


async def read_course_by_id(course_id: int, session: AsyncSession = Depends(get_session)):
    """Получение курса по id"""
    course = await session.get(Course, course_id)
    if course:
        return course
    return None


async def read_courses_count(session: AsyncSession = Depends(get_session)):
    """Получение количества курсов"""
    request = select(Course.id)
    result = await session.execute(request)
    courses_count = result.scalar_one()
    return courses_count
