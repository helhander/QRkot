from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import PreCharityBase


class Donation(PreCharityBase):
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)
