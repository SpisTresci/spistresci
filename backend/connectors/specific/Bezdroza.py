from connectors.common import HelionBase, HelionBaseBook
from sqlwrapper import *

class Bezdroza(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class BezdrozaBook(HelionBaseBook, Base):
    pass
