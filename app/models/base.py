from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class PreCharityBase(Base):
    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    close_date = Column(DateTime)
