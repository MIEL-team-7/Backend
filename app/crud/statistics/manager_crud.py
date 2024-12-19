from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timedelta

from app.models.models import Candidate, Manager, Course, CandidateCourse, Office
from app.utils.database.test_data import get_session


async def read_quotas_by_manager_id(manager_id: int, session: AsyncSession = Depends(get_session)):
    """Получение числа квот руководителя"""
    request = select(Manager.quotas).filter(Manager.id == manager_id)
    result = await session.execute(request)
    quotas = result.scalar_one()
    if quotas:
        return quotas
    return None


async def read_managers_count(id: int, session: AsyncSession = Depends(get_session)):
    """Получение числа руководителей"""
    manager = await session.execute(select(func.count()).select_from(Manager))
    if manager:
        return manager
    return None
