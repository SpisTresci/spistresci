from sqlwrapper import *
from connectors.common import KsiazkiFabrykaBase, KsiazkiFabrykaBaseBook

Base = SqlWrapper.getBaseClass()
class Fabryka(KsiazkiFabrykaBase):
    title_suffix= ' [e-book]'

#{'raw_title': 150, 'description': 17690, 'price': 6, 'page_count': 4, 'sample': 39, 'authors': 228, 'date': 4, 'availability': 1, 'category': 70, 'publisher': 25, 'title': 150, 'url': 208, 'cover': 112, 'isbns': 17, 'formats': 13, 'external_id': 11}

class FabrykaBook(KsiazkiFabrykaBaseBook, Base):
    pass