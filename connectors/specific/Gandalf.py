from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Gandalf(Ceneo):
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('@id', ''),
        'url':('@url', ''),
        'price':('@price', 0),
        'availability': ('@avail', ''),
        'category':('./cat', ''),
        'title':('./name', ''),
        'cover':("./imgs/main[@url]", ''),
        'description':('./desc', ''),

        'authors':("./attrs/a[@name='Autor']", ''),
        'isbns':("./attrs/a[@name='ISBN']", ''),
        #'eans':("./attrs/a[@name='EAN']", ''), this information like ISBN, but in different format
        'formats':("./attrs/a[@name='Format']", ''),
        'page_count':("./attrs/a[@name='Ilosc_stron']", ''),
        'cover_type':("./attrs/a[@name='Oprawa']", ''),
        'publisher':("./attrs/a[@name='Wydawnictwo']", ''),
    }

    def weHaveToGoDeeper(self, root, depth):
        return root.xpath("./group[@name='books']")[0]

class GandalfBook(GenericBook, Base):
    #external_id
    url = Column(Unicode(128))          #81
    #price
    availability = Column(Integer)
    category = Column(Unicode(64))      #53
    title = Column(Unicode(256))        #208
    cover = Column(Unicode(128))        #93
    #description
    #authors
    #isbns
    #formats
    page_count = Column(Integer)
    cover_type =  Column(Unicode(64))   #30
    publisher = Column(Unicode(128))    #61
