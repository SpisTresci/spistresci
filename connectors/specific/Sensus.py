from connectors.generic import *
from connectors.common import HelionBase, HelionBaseBook
import lxml.etree as et
from sqlwrapper import *


class Sensus(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class SensusBook(HelionBaseBook, Base):
    pass