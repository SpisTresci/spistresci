from connectors.common import HelionBase, HelionBaseBook
from sqlwrapper import SqlWrapper

class DlaBystrzakow(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class DlaBystrzakowBook(HelionBaseBook, Base):
    pass
