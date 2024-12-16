from idlelib.debugger_r import DictProxy

from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.statistics.candidate_crud import read_candidate_count
from app.models.models import Candidate, Manager, Office
from app.utils.database.test_data import get_session


async def get_offices(session: AsyncSession = Depends(get_session)):
    """Получение всех офисов"""
    request = select(Office)
    result = await session.execute(request)
    all_offices = result.scalars().all()
    return all_offices


async def get_office_by_id(id: int, session: AsyncSession = Depends(get_session)):
    """Получение офисов в городе"""
    office = await session.get(Office, id)
    if office:
        return office
    return None


async def get_quotas_by_manager_id(manager_id: int, session: AsyncSession = Depends(get_session)):
    request = select(Manager.quotas).filter(Manager.id == manager_id)
    result = await session.execute(request)
    quotas = result.scalar_one()
    if quotas:
        return quotas
    return None


async def get_office_load(manager_id: int, session: AsyncSession = Depends(get_session)):
    total_candidates = read_candidate_count(),
    quotas = get_quotas_by_manager_id(manager_id, session),
    available_slots = quotas - total_candidates
    return {
        "total": total_candidates,
        "quotas": quotas,
        "available_slots": available_slots,
    }