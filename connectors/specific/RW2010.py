from connectors.generic import XMLConnector
import os
from sqlwrapper import *
from connectors.generic import GenericBook
import urllib2

class RW2010(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './tytul':('title', ''),
        './url':('url', ''),
        './autor':('authors', ''),
        './formaty':('formats', ''),
        './okladka':('cover', ''),
        './cena':('price', 0),
    }

    def __init__(self, name = "RW2010", limit_books = 0):
        super(RW2010, self).__init__(name = name, limit_books = limit_books)
        self.macro_url = self.config['macro_url']
        u = urllib2.urlopen(self.macro_url)
        meta = u.info()
        result = u.read()
        u.close()
        if result != 'Ok.':
            raise Exception('RW2010 init, macro %s returned %s' % (self.macro_url, result))

    def adjust_parse(self, dic):
        self.create_id_from_url(dic)

    def create_id_from_url(self, dic):
        url = dic['url']
        let_id = url.split('/')[6].replace("%3D", "").replace(".html", "")
        base = ord('z') - ord("0") + 1

        repr = 0
        i = 0
        for let in let_id[::-1]:
            digit = ord(let) - ord('0')
            repr += (digit * pow(base, i))
            i = i + 1

    #    print repr
    #    print let_id
    #    print self.recreate_str_id_from_id(repr)
        assert let_id == self.recreate_str_id_from_id(repr)
        dic['external_id'] = unicode(repr)

    def recreate_str_id_from_id(self, str):
        int_id = int(str)
        base = ord('z') - ord("0") + 1

        str_repr = ""

        while True:
            let = int_id % base
            str_repr = str_repr + chr(let + ord('0'))
            int_id = int_id / base
            if int_id == 0:
                break

        word = str_repr[::-1]
        return word

Base = SqlWrapper.getBaseClass()

class RW2010Book(GenericBook, Base):
    #title
    url = Column(Unicode(160))          #155
    #authors
    cover = Column(Unicode(160))        #150
    price = Column(Integer)             #GROSZE!!!
