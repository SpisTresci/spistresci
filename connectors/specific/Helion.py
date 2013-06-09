from connectors.generic import *
from connectors.common import HelionBase, HelionBaseBook
import lxml.etree as et
from sqlwrapper import *


class Helion(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class HelionBook(HelionBaseBook, Base):
    pass
