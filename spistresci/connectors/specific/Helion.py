from connectors.common import HelionBase, HelionBaseBook
from sqlwrapper import SqlWrapper

class Helion(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class HelionBook(HelionBaseBook, Base):
    pass
