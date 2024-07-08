"""
This is the module that contains my organisation model
"""

from . import Base
from sqlalchemy import Column, String
from uuid import uuid4


class OrganisationModel(Base):
    __tablename__ = 'organisation_info'

    orgId = Column(String(50), primary_key=True, default=str(uuid4()), unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String(2550), nullable=False)

    def to_dict(self):
        return {
            'orgId': self.orgId,
            'name': self.name,
            'description': self.description
        }
