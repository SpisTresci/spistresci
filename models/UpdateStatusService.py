from sqlwrapper import *
from models.Service import Service
import time

Base = SqlWrapper.getBaseClass()

class UpdateStatusService(Base):
    __tablename__ = "UpdateStatusService"

    id = Column(Integer, primary_key=True)
    update_status_id = Column(Integer, ForeignKey('UpdateStatus.id'))

    service_name = Column(Unicode(32), ForeignKey('Service.name'))
    service = relationship('Service', uselist=False)

    success = Column(Boolean, default=False)

    checksum = Column(Unicode(32))

    offers = Column(Integer)
    offers_parsed = Column(Integer)
    offers_new = Column(Integer)
    offers_promotion = Column(Integer)

    timestamp = Column(Integer)

    fetch_start = Column(DateTime)
    fetch_end = Column(DateTime)

    parse_start = Column(DateTime)
    parse_end = Column(DateTime)

    final_start = Column(DateTime)
    final_end = Column(DateTime)

    session = None

    def __init__(self, us, connector):
        self.timestamp = int(time.time())
        us.update_status_services.append(self)
        self.service = Service.get_or_create(connector, session = us.session)
        connector.update_status_service = self
        self.session = us.session

SqlWrapper.table_list += [UpdateStatusService.__tablename__]
