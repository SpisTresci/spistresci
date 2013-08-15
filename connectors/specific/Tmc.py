from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Tmc(Afiliant):
    xml_tag_dict = dict (Afiliant.xml_tag_dict.items() + [('publisher', ("./n:attribute[name='Producent']/value", ''))])

class TmcBook(GenericBook, Base):
    pass
