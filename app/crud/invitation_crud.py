from app.crud.manager_crud import read_manager_by_id, read_candidate_by_id
from app.models.models import (
      ManagerCandidate,
)
from app.core.logging import logger
from fastapi import HTTPException
from starlette import status

async def invite_candidate(current_user_id, session, candidate_id):
    if await check_quotas(current_user_id, session):
        invitation = await create_invitation(current_user_id, session, candidate_id.id)
        return invitation
    else:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Not enough quotas to send invites"
            )

async def check_quotas(current_user_id, session):
    manager = await read_manager_by_id(current_user_id, session)
    if manager.quotas > 0:
        return True

async def create_invitation(current_user_id, session, candidate_id):
    manager = await read_manager_by_id(current_user_id, session)
    create_obj_invite = ManagerCandidate(candidate_id=candidate_id, done_by=current_user_id)
    manager.quotas = manager.quotas - 1
    candidate = await read_candidate_by_id(candidate_id, session)
    candidate.is_hired = True # FIXME Кандидат не становиться нанятым, он только приглашается. Кроме того, нет отслеживания ошибок(если пользователь не найден)
    session.add(create_obj_invite)
    await session.commit()
    await session.refresh(create_obj_invite)
    await session.refresh(manager)
    await session.refresh(candidate)
    return create_obj_invite