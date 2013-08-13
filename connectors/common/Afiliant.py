from connectors.generic import XMLConnector
import lxml.etree as et
from connectors.generic import *
import os

class Afiliant(XMLConnector):

    xmls_namespace = {'n':'urn:ExportB2B'}
    depth = 3

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {-
        'external_id': ('./n:id', ''),
        'price': ('./n:price', 0),
        'title': ('./n:name', ''),
        'url': ('./n:url', ''),
        'category': ('./n:categoryId', ''),
        'description': ('./n:description', ''),
        'cover': ('./n:image', ''),
        'isbn' : ("./n:attribute@name='ISBN']/value", ''),
    }

