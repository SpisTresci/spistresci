from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Legimi(Afiliant):
    xml_tag_dict = dict(Afiliant.xml_tag_dict.items() + [
        ('authors', ("./n:attributes/n:attribute[n:name='Autor']/n:value", '')),
        ('formats', ("./n:attributes/n:attribute[n:name='Format']/n:value", '')),
        ('publisher', ("./n:attributes/n:attribute[n:name='Wydawnictwo']/n:value", '')),
        ('date', ("./n:attributes/n:attribute[n:name='Rok_wydania']/n:value", '')),
        ('isbns', ("./n:attributes/n:attribute[n:name='ISBN']/n:value", '')),
        ('subscription', ("./n:attributes/n:attribute[n:name='Abonament']/n:value", '')),
    ] )

class LegimiBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    #external_id = Column(Integer, unique=True)
    #title
    #price
    #price_normal
    url = Column(Unicode(128))           #60
    cover = Column(Unicode(64))         #52
    category = Column(Unicode(128))      #82
    publisher = Column(Unicode(128))     #73
    date = Column(Unicode(4))           #4

