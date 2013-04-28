from connectors.generic import *
import lxml.etree as et
import urllib2
import os
from sqlwrapper import *

class Czytio(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './id':('external_id', None),
        './title':('title', ''),
        './url':('url', ''),
        './authors':('authors', ''),
        './format':('format', ''),
        './isbn':('isbn', ''),
        './cover':('cover', ''),
        './price':('price', 0),
        './size':('size', 0),
    }

Base = SqlWrapper.getBaseClass()

class CzytioBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    #title
    url = Column(Unicode(120))          #109
    #authors
    format = Column(Unicode(4))         #4
    isbn = Column(Unicode(25))          #20, 978-83-02-63935-07-8
    cover = Column(Unicode(128))        #118
    price = Column(Integer)             #GROSZE!!!
    size = Column(Integer)             #GROSZE!!!


class CzytioBookDescription(GenericBookDescription, Base):
    pass

class CzytioAuthor(GenericAuthor, Base):
    pass

class CzytioBookPrice(GenericBookPrice, Base):
    pass

class CzytioBooksAuthors(GenericBooksAuthors, Base):
    pass

#{'isbn': 20, 'format': 4, 'url': 109, 'price': 6, 'title': 255, 'cover': 118, 'authors': 3, 'external_id': 5, 'size': 8}
#isbn: 978-83-02-63935-07-8
#title:
#url: http://www.czytio.pl/ksiegarnia/ebook/100751/Might_Magic_Heroes_VI_-_prolog_mechanika_wskazowki_-_poradnik_do
#price: 179.10
#format: EPUB
#cover: http://www.czytio.pl/ksiegarnia/images/309/100727-Zyj_pelnia_zycia_pomimo_niesmialosci_i_leku_W_drodze_do_pewnosci.jpg
#authors: [u'Mark Twain', u'Milena Lisiecka', u'Micha\u0142 Filipczuk']
#external_id: 22635
#size: 1 019 KB
