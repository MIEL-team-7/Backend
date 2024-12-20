
from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.statistics.candidate_crud import read_candidate_count
from app.crud.statistics.manager_crud import read_quotas_by_manager_id
from app.models.models import Office
from app.utils.database.test_data import get_session


async def read_offices_count(session: AsyncSession = Depends(get_session)):
    """Получение количества всех офисов"""
    request = select(func.count()).select_from(Office)
    result = await session.execute(request)
    all_offices = result.scalar_one()
    return all_offices


async def read_office_load(
    office_id: int, session: AsyncSession = Depends(get_session)
):
    """Получение загруженности офиса по id офиса"""
    request = await session.execute(select(Office).where(Office.id == office_id))
    office = request.scalars().first()

    if not office:
        return None

    total_candidates = await read_candidate_count(
        session
    )  # FIXME: функция возвращает общее количество кандидатов. Этот пункт не нужен, так как офисы не имеют квоты. Их имеют руководители.
    quotas = await read_quotas_by_manager_id(
        office_id, session
    )  # FIXME: функция запрашивает manager_id(id руководителя), а не office_id(id офиса)
    available_slots = quotas - total_candidates

    return {
        "name": office.name,
        "location": office.location,
        "total": total_candidates,
        "quotas": quotas,
        "available_slots": available_slots,
    }


async def read_all_offices_load(session: AsyncSession = Depends(get_session)):
    """Получение загруженности всех офисов"""
    # Извлечение всех идентификаторов офисов
    result = await session.execute(select(Office.id))
    office_ids = result.scalars().all()

    # Список для хранения статистики по всем офисам
    offices_stats = []

    # Обход каждого офиса и получение его статистики
    for office_id in office_ids:
        office_load = await read_office_load(office_id, session)
        offices_stats.append(office_load)

    return offices_stats


async def read_office_by_id(
    office_id: int, session: AsyncSession = Depends(get_session)
):
    """Получение офиса по id"""
    request = select(Office)
    result = await session.execute(request)
    office = result.scalars().all()
    return office
