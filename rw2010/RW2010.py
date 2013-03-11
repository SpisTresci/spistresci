from generic import *
from xml.etree import ElementTree as et
import urllib2
import os
from sql_wrapper import *

class RW2010(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'tytul':('title',''),
        'url':('url',''),
        'autor':('authors',''),
        'formaty':('format',''),
        'okladka':('cover',''),
        'cena':('price',0),
    }

    def __init__(self, name, limit_books=0):
        XMLConnector.__init__(self, name=name, limit_books=limit_books)
        self.macro_url = self.config['macro_url']
        u = urllib2.urlopen(self.macro_url) 
        meta = u.info()
        result = u.read()
        u.close()
        if result!= 'Ok.':
            raise Exception('RW2010 init, macro %s returned %s'%(self.macro_url,result))

    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        offers = list(root)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            #print dic
            self.create_id_from_url(dic)
            self.validate(dic)
            #print dic
            #self.mesureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key+": "+ unicode(self.max_len_entry[key])

    def create_id_from_url(self, dic):
        url = dic['url']
        let_id=url.split('/')[6].replace("%3D","").replace(".html","")
        base=ord('z')-ord("0")+1

        repr=0
        i=0
        for let in let_id[::-1]:
            digit=ord(let)-ord('0')
            repr=repr + (digit * pow(base,i))
            i=i+1

        print repr
        print let_id
        print self.recreate_str_id_from_id(repr)
        assert let_id == self.recreate_str_id_from_id(repr)
        dic['external_id']=unicode(repr)

    def recreate_str_id_from_id(self, str):
        int_id=int(str)
        base=ord('z')-ord("0")+1

        str_repr=""

        while True:
            let=int_id%base
            str_repr = str_repr + chr(let+ord('0'))
            int_id = int_id/base
            if int_id == 0:
                break

        word=str_repr[::-1]
        return word


Base = SqlWrapper.getBaseClass()

class RW2010Book(GenericBook, Base):
    #title
    url = Column(Unicode(160))          #155
    #authors
    format = Column(Unicode(15))         #15
    isbn = Column(Unicode(13))          #0
    cover = Column(Unicode(160))        #150
    price = Column(Integer)             #GROSZE!!!


class RW2010BookDescription(GenericBookDescription, Base):
    pass

class RW2010Author(GenericAuthor, Base):
    pass

class RW2010BookPrice(GenericBookPrice, Base):
    pass

class RW2010BooksAuthors(GenericBooksAuthors, Base):
    pass

#{'authors': 12, 'isbn': 0, 'format': 15, 'url': 155, 'price': 4, 'title': 98, 'cover': 150}
#isbn:
#title: Nie nadaje sie na zolnierza, to jeszcze szczeniak. Tajna historia II wojny swiatowej, ilustrowana.
#url: http://www.rw2010.pl/go.live.php/PL-H6/przegladaj/SMjM3/nie-nadaje-sie-na-zolnierza-to-jeszcze-szczeniak-tajna-historia-ii-wojny-swiatowej-ilustrowana.html
#price: 1000
#format: pdf, epub, mobi
#cover: http://www.rw2010.pl/data/catalogue/StLS00NzM2NTMtUG93cm90eSB3IHRvbmFjamkgc2NpLWZpX09LxYFBREtBIFBSWsOTRF9QaW90ciBLaWXFgmJpZXdza2lfNzExeDEwMjQuanBn.jpg
#authors: [u'Samuel', u'Gizmo', u'Jula', u'Kocica', u'Maciej', u'Klara', u'Magdalena', u'Miron', u'Simon', u'Adrian', u'Dorian', u'Irmina.']
