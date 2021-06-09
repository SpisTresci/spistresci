from connectors.common import HelionBase, HelionBaseBook
from sqlwrapper import SqlWrapper

class eBookpoint(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class eBookpointBook(HelionBaseBook, Base):
    pass

