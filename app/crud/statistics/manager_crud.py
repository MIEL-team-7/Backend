from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timedelta

from app.models.models import Candidate, Manager, Course, CandidateCourse
from app.utils.database.test_data import get_session


async def read_quotas_by_manager_id(manager_id: int, session: AsyncSession = Depends(get_session)):
    request = select(Manager.quotas).filter(Manager.id == manager_id)
    result = await session.execute(request)
    quotas = result.scalar_one()
    if quotas:
        return quotas
    return None


async def read_manager_by_id(id: int, session: AsyncSession = Depends(get_session)):
    """Поиск руководителя по id"""
    manager = await session.get(Manager, id)
    if manager:
        return manager
    return None
