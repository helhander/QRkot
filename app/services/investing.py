from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models import CharityProject, Donation


async def run_investing(
    session: AsyncSession,
    charity_project: Optional[CharityProject] = None,
    donation: Optional[Donation] = None,
) -> None:
    actual_donations = await session.execute(
        select(Donation)
        .where(Donation.fully_invested == false())
        .order_by(Donation.create_date.desc(), Donation.id.desc())
    )
    donations = actual_donations.scalars().all()

    actual_charity_projects = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested == false())
        .order_by(CharityProject.create_date.desc(), CharityProject.id.desc())
    )
    charity_projects = actual_charity_projects.scalars().all()

    charity_project_left = 0
    donation_left = 0

    while (
        len(donations) > 0 and
        (charity_project_left > 0 or len(charity_projects) > 0) or
        len(charity_projects) > 0 and
        donation_left > 0
    ):
        if charity_project_left == 0:
            cur_charity_project = charity_projects.pop()
            session.add(cur_charity_project)
            charity_project_left = (
                cur_charity_project.full_amount -
                cur_charity_project.invested_amount
            )

        if donation_left == 0:
            cur_donation = donations.pop()
            session.add(cur_donation)
            donation_left = (
                cur_donation.full_amount - cur_donation.invested_amount
            )

        if donation_left <= charity_project_left:
            cur_donation.fully_invested = True
            cur_donation.invested_amount = cur_donation.full_amount
            cur_donation.close_date = datetime.now()
            cur_charity_project.invested_amount += donation_left
            charity_project_left -= donation_left
            donation_left -= donation_left

        if donation_left >= charity_project_left:
            cur_charity_project.fully_invested = True
            cur_charity_project.close_date = datetime.now()
            if donation_left != charity_project_left:
                cur_charity_project.invested_amount = (
                    cur_charity_project.full_amount
                )
                cur_donation.invested_amount += charity_project_left
                donation_left -= charity_project_left
                charity_project_left -= charity_project_left

    await session.commit()
    if charity_project is not None:
        await session.refresh(charity_project)
    if donation is not None:
        await session.refresh(donation)
