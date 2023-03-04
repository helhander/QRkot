from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    async def get_charity_project_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict]:
        charity_projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description,
            ).where(CharityProject.fully_invested == True)
        )
        charity_projects = charity_projects.all()
        charity_projects = [
            {
                'name': p['name'],
                'collecting_time': p['close_date'] - p['create_date'],
                'description': p['description'],
            }
            for p in charity_projects
        ]
        sorted(charity_projects, key=lambda p: p['collecting_time'])
        return charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)
