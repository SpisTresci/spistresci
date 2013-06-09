from connectors.generic import *
from connectors.common import HelionBase, HelionBaseBook
import lxml.etree as et
from sqlwrapper import *


class Bezdroza(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class BezdrozaBook(HelionBaseBook, Base):
    pass