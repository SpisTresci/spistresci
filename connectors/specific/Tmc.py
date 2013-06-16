from connectors.common import Afiliant
from connectors.generic import GenericBook
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class Tmc(Afiliant):
    pass

class TmcBook(GenericBook, Base):
    pass
