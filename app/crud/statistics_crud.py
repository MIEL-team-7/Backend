from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Candidate, Manager
from app.utils.database.test_data import get_session


async def get_candidate_count(id: int, session: AsyncSession = Depends(get_session)):
    # candidate = await session.execute("SELECT COUNT(*) FROM candidates").fetchone()
    candidate = await session.get(Candidate, id)
    if candidate:
        return candidate
    return None

async def get_manager_count(id: int, session: AsyncSession = Depends(get_session)):
    # manager = await session.execute("SELECT COUNT(*) FROM managers").fetchone()
    manager = await session.get(Manager, id)
    if manager:
        return manager
    return None
