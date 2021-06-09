from connectors.common import HelionBase, HelionBaseBook
from sqlwrapper import SqlWrapper

class OnePress(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class OnePressBook(HelionBaseBook, Base):
    pass

