from connectors.generic import *
from connectors.common import HelionBase, HelionBaseBook
import lxml.etree as et
from sqlwrapper import *


class eBookpoint(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class eBookpointBook(HelionBaseBook, Base):
    pass