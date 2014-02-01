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

class Booki24Book(GenericBook, Base):
	pass
