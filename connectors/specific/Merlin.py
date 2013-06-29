from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Merlin(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./dzial":('section', ''),
        "./dzial_id":('section_id', ''),
        "./towar_id":('external_id', ''),
        "./identyfikator":('isbns', ''),
        "./url":('url', ''),
        "./url_images":('cover', ''),
        "./url_koszyk":('add_to_cart_url', ''),
        "./utm_term":('utm_term', ''), #?
        "./tytul":('title', ''),
        "./status":('status', ''),  #?
        "./date":('date', ''),  #?
        "./liczba_stron":('page_count', ''),  #?
        "./jezyk":('lang', ''),  #?
        "./cena":('price', ''),
        "./opis":('description', ''),
        "./lista_kategorii":('category', ''),
        "./wydawnictwo":('publisher', ''),
        "./autor":('authors', ''),
        "./tlumacz":('translators', ''),
        "./redakcja":('redactor', ''),
        "./nosnik":('formats', ''),
    }

    def validate(self, dic):
        self.validateTitle(dic)
        super(Merlin, self).validate(dic)

    def validateISBNs(self, dic, id, title):
        if dic.get("isbns"):
            i = dic["isbns"]
            formats = ['PDF', 'EPUB', 'MOBI', 'MP3']

            for f in formats:
                if i.endswith('_' + f):
                    i = i.replace('_' + f, '')
            dic["isbns"] = i

        super(Merlin, self).validateISBNs(dic, id, title)

    def validateTitle(self, dic):
        if dic.get("title"):
            t = dic["title"]
            formats = ['PDF', 'EPUB', 'MOBI', 'MP3', #typical
                       'mp3', 'format mp3', 'audiobook', 'pdf' #few exceptions
                       ]

            for f in formats:
                if (' (' + f + ')') in t:
                    t = t.replace(' (' + f + ')', '')
            dic['title'] = t

class MerlinBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    section = Column(Unicode(16))           #9
    section_id = Column(Integer)
    #external_id
    #isbns
    url = Column(Unicode(64))               #59
    cover = Column(Unicode(64))             #62
    add_to_cart_url = Column(Unicode(512))  #412
    utm_term = Column(Unicode(256))         #248
    title = Column(Unicode(256))            #220
    status = Column(Unicode(2))             #1
    date = Column(Unicode(16))              #
    page_count = Column(Unicode(8))         #6
    lang = Column(Unicode(16))              #32
    #price
    #description
    category = Column(Unicode(256))         #165
    publisher = Column(Unicode(73))         #128
    #authors
    #redactor - TODO: add support
    #formats
