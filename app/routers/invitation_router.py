from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.crud.invitation_crud import invite_candidate

from app.utils.authentication import get_current_user
from app.schemas.manager_schema import inviteCandidate

invitation_of_manager = APIRouter(
    prefix="/invitation",
    tags=["Работа с руководителем"],
)


@invitation_of_manager.post("/invite_candidate/")
async def invite_candidate_of_manager(
    current_user_id: Annotated[int, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    candidate: inviteCandidate,
):
    invitation = await invite_candidate(current_user_id, session, candidate)
    return invitation
