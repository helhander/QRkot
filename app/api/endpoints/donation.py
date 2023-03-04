from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.services.investing import run_investing

router = APIRouter()


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    await run_investing(session, donation=new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUser],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    all_donations = await donation_crud.get_by_user(user, session)
    return all_donations


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations
