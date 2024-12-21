from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.statistics.office_crud import read_office_load, read_office_by_manager_id
from app.models.models import Manager
from app.utils.database.test_data import get_session


async def read_manager_by_id(manager_id: int, session: AsyncSession = Depends(get_session)):
    """Получение руководителя по id"""
    request = select(Manager).where(Manager.id == manager_id)
    result = await session.execute(request)
    manager = result.scalars().first()
    if manager:
        return manager
    return None


async def read_quotas_by_manager_id(manager_id: int, session: AsyncSession = Depends(get_session)):
    """Получение числа квот руководителя"""
    request = select(Manager.quotas).filter(Manager.id == manager_id)
    result = await session.execute(request)
    quotas = result.scalar_one()
    if quotas:
        return quotas
    return None


async def read_managers_count(session: AsyncSession = Depends(get_session)):
    """Получение числа руководителей"""
    manager = await session.execute(select(func.count()).select_from(Manager))
    if manager:
        return manager
    return None


async def read_manager_statistics(manager_id: int, session: AsyncSession = Depends(get_session)):
    """Получение статистики руководителя"""
    request = select(Manager.id, Manager.full_name, Manager.office_id)
    result = await session.execute(request)
    managers = result.scalars().all()

    manager_statistics = []
    for id, full_name, office_id in managers:
        office_load = read_office_load(office_id)
        tmp = {
            "full_name": full_name,
            "office": office_load,
        }
        manager_statistics.append(tmp)

    return manager_statistics
