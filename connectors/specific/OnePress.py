from connectors.generic import *
from connectors.common import HelionBase, HelionBaseBook
import lxml.etree as et
from sqlwrapper import *


class OnePress(HelionBase):
    pass

Base = SqlWrapper.getBaseClass()
class OnePressBook(HelionBaseBook, Base):
    pass