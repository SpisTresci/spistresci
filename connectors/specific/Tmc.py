from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Tmc(Afiliant):
    xml_tag_dict = Afiliant.xml_tag_dict + {
        'publisher' : ("./n:attribute[name='Producen']/value", ''),
    }

class TmcBook(GenericBook, Base):
    pass
