from sqlwrapper import SqlWrapper
from sqlalchemy.orm import sessionmaker

config_db_file = 'unittests/data/db/update/conf/test_db.ini'

class LocalSqlWrapper(SqlWrapper):
    session = None

    @classmethod
    def getSession(cls):
        if not cls.session:
            cls.session = sessionmaker(bind=cls.getEngine(), autoflush=False)()
        return cls.session

def setup_package(package):
    LocalSqlWrapper.init(config_file=config_db_file, connectors=["Audiobook"])

def teardown_package(package):
    LocalSqlWrapper.getSession().close()
    LocalSqlWrapper.getBroadEngine().execute("DROP DATABASE st_unittests")
