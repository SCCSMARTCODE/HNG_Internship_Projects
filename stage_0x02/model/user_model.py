"""
This is the module that contains my user model
"""

from . import Base
from sqlalchemy import Column, String
from uuid import uuid4


class UserModel(Base):
    __tablename__ = 'user_info'

    userId = Column(String(50), primary_key=True, default=str(uuid4()), unique=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(255))

    def to_dict(self):
        return {
            'userId': self.userId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'phone': self.phone
        }


