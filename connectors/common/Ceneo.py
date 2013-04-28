from connectors.generic import XMLConnector
import lxml.etree as et
from connectors.generic import *
import os
import re

class Ceneo(XMLConnector):
    depth=1

class CeneoBook(GenericBook):
    pass

class CeneoBookDescription(GenericBookDescription):
    pass

class CeneoAuthor(GenericAuthor):
    pass

class CeneoBookPrice(GenericBookPrice):
    pass

class CeneoBooksAuthors(GenericBooksAuthors):
    pass
