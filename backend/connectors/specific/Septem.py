from connectors.common import HelionBase, HelionBaseBook
from sqlwrapper import SqlWrapper

class Septem(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class SeptemBook(HelionBaseBook, Base):
    pass
