from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Booki24(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('./id', None),
        'title': ('./name', ''),
        'publisher':('./manufacturer', ''),
        'description': ('./description', ''),
        'price': ('./price', 0),
        'url': ('./url', ''),
        'cover': ('./cover', ''),
        'isbns': ('./isbn', ''),
        'authors': ('./author/authors', ''),
        'categories': ('./categories/category', ''),
        'formats': ('./formats/format[@name]', ''),
    }

Base = SqlWrapper.getBaseClass()


# {'publisher': 108, 'description': 16636, 'title': 255, 'url': 287, 'price': 6, 'authors': 0, 'cover': 297, 'isbns': 17, 'formats': 4, 'external_id': 5, 'categories': 28}
class Booki24Book(GenericBook, Base):
    #external_id
    #title
    publisher = Column(Unicode(128))
    #description
    #price
    #url
    #cover
    #isbns
    ##categories -  #TODO
    #formats
