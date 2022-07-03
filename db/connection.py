from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()
metadata = Base.metadata


class Db:

    def __init__(self, host, db, username, password, socket=None, port=None):
        self.host = host
        self.database = db
        self.username = username
        self.password = password
        self.port = port
        self.socket = socket
        self.database_uri = self.get_connection_uri()
        self.engine = self.get_engine()
        self.database_session = self.get_db_session()

    def get_connection_uri(self):
        return "mysql+pymysql://{username}:{password}@{host}/{db}?charset=utf8&binary_prefix=true".format(
            username=self.username,
            password=self.password,
            host=self.host,
            db=self.database,
            # socket=self.socket
        )

    def get_engine(self):
        return create_engine(self.database_uri, poolclass=NullPool)

    def get_db_session(self):
        return scoped_session(
            sessionmaker(autocommit=False,
                         autoflush=True,
                         bind=self.engine)
        )

    def close(self):
        try:
            self.database_session.remove()
            self.engine.dispose()
        except Exception as e:
            pass