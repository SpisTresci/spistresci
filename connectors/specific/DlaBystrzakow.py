from connectors.generic import *
from connectors.common import HelionBase, HelionBaseBook
import lxml.etree as et
from sqlwrapper import *


class DlaBystrzakow(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class DlaBystrzakowBook(HelionBaseBook, Base):
    pass