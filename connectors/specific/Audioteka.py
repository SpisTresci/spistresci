# vim: set fileencoding=utf-8
from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook


Base = SqlWrapper.getBaseClass()

class Audioteka(Afiliant):

    #note: what we do here is defining new xml_tag_dict by creating dict from list of (key,value) tuples
    xml_tag_dict = dict(Afiliant.xml_tag_dict.items() + [
        ('authors', (u"./n:attributes/n:attribute[n:name='Autor']/n:value", '')),
        ('publisher', (u"./n:attributes/n:attribute[n:name='Wydawca']/n:value", '')),
        ('length', (u"./n:attributes/n:attribute[n:name='Dugość']/n:value", '')),
        ('lectors', (u"./n:attributes/n:attribute[n:name='Czyta']/n:value", '')),
    ])

class AudiotekaBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    external_id = Column(Unicode(128), unique = True) #86
    #title
    #price
    #price_normal
    url = Column(Unicode(128))          #60
    #cover = Column(Unicode(256))       #145
    category = Column(Unicode(32))      #21
    publisher = Column(Unicode(128))    #79
    length = Column(Unicode(32))        #16
