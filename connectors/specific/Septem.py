from connectors.generic import *
from connectors.common import HelionBase, HelionBaseBook
import lxml.etree as et
from sqlwrapper import *


class Septem(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class SeptemBook(HelionBaseBook, Base):
    pass