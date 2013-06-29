from connectors.common import HelionBase, HelionBaseBook
from sqlwrapper import SqlWrapper

class Sensus(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class SensusBook(HelionBaseBook, Base):
    pass

