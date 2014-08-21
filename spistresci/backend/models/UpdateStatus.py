from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class UpdateStatus(Base):
    __tablename__ = "UpdateStatus"

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    manual = Column(Boolean)
    partial = Column(Boolean)
    update_status_services = relationship("UpdateStatusService")
    finished = Column(Boolean, default=False)
    success = Column(Boolean, default=False)

    session = None
    def __init__(self, session = None):
        self.session = session if session else sessionmaker(bind = SqlWrapper.getEngine(), autoflush=True)()
        self.session.add(self)

SqlWrapper.table_list += [UpdateStatus.__tablename__]
