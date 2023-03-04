from sqlalchemy import Column, String, Text

from .base import PreCharityBase


class CharityProject(PreCharityBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
