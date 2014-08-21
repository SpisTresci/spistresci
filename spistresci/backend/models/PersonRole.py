from sqlwrapper import *
from utils.GetOrCreateCache import GetOrCreateCache

Base = SqlWrapper.getBaseClass()

class PersonRole(GetOrCreateCache, Base):
    __tablename__ = "PersonRole"

    name = Column(Unicode(15), primary_key=True)

    @classmethod
    def init_rows(cls):
        from utils import DataValidator
        session = sessionmaker(bind=SqlWrapper.getEngine())()
        for role in DataValidator.supported_persons:
            session.add(PersonRole(name=role))
        session.commit()

SqlWrapper.table_list += [PersonRole.__tablename__]