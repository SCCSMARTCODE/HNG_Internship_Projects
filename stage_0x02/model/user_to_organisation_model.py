"""
This is the module that contains my  Organisations To Users Model
"""

from . import Base
from sqlalchemy import Column, String, Boolean, ForeignKey
from uuid import uuid4


class UserToOrganisationModel(Base):
    __tablename__ = 'user_to_organisation_info'

    id = Column(String(50), primary_key=True, default=str(uuid4()), unique=True)
    userId = Column(String(50), ForeignKey('user_info.userId'), nullable=False)
    orgId = Column(String(50), ForeignKey('organisation_info.orgId'), nullable=False)
    isCreator = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'orgId': self.orgId,
            'isCreator': self.isCreator
        }
