from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Tmc(Afiliant):
    pass

class TmcBook(GenericBook, Base):
    pass
