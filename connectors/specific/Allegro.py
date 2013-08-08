from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Allegro(Ceneo):
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('@id', ''),
        'price':('@price', 0),
        'url':('@url', ''),
        'availability': ('@avail', ''),
        'title':('./name', ''),
        'category':('./cat', ''),
        'cover':("./imgs/main[@url]", ''),
        'description':('./desc', ''),
        'authors':("./attrs/a[@name='Autor']", ''),
        'isbns':("./attrs/a[@name='ISBN']", ''),
        'publisher':("./attrs/a[@name='Wydawnictwo']", ''),
        'date':("./attrs/a[@name='Rok_Wydania']", ''),
        'formats':("./attrs/a[@name='Format']", ''),
    }

    format_convertions_rules = [
        (r"MOBI\(Kindle\)", "MOBI")
    ]


class AllegroBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    #external_id

    #price = Column(Integer)
    #price_normal

    #url = Column(Unicode(256))
    availability = Column(Integer)
    #title = Column(Unicode(256))
    category = Column(Unicode(64))
    cover = Column(Unicode(128))
    #description
    #authors
    #isbns
    date = Column(Date(64))
    #formats
