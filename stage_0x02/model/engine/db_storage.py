"""
This is the module that contains the project engine
    class = DBStorage
"""

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from model.user_model import UserModel
from model.organisation_model import OrganisationModel
from model.user_to_organisation_model import UserToOrganisationModel
from model import Base
import logging
import os

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

ca_cert_pat = os.path.join(os.getcwd(), 'ca.pem')


class DBStorage(object):
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(
            "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                os.getenv('HNG_STAGE2_USER'),
                os.getenv('HNG_STAGE2_USER_PW'),
                os.getenv('HNG_STAGE2_USER_DB_HOST'),
                os.getenv('HNG_STAGE2_USER_DB_PORT'),
                os.getenv('HNG_STAGE2_USER_DB_NAME')
            ),
            connect_args={
                'sslmode': 'require',
                'sslrootcert': ca_cert_pat
            },
            pool_recycle=3600,
            echo=True,
            echo_pool=True,
            pool_size=5,
            max_overflow=10
        )

        session = sessionmaker(self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session
        Base.metadata.create_all(self.__engine)

    def session(self):
        return self.__session


if __name__ == '__main__':
    engine = DBStorage()
