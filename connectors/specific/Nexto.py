from connectors.generic import XMLConnector
from connectors.generic import *
from sqlwrapper import *
import lxml.etree as et
import os
import urllib, urllib2

class Nexto(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './id':('external_id', None),
        './isbn':('isbn', ''),
        './language':('lang_short', ''),
        './body':('description', ''),
        './title':('title', ''),
        './publisher':('publisher', ''),
        './manufacturer_id':('manufacturer_id', ''),
        './product_code':('product_code', ''),

        './category_refs/id':('category_id', ''),

        './issues/issue/issue_id':('issue_id', ''),
        './issues/issue/author':('authors', ''),
        './issues/issue/gross_nexto_price':('gross_price', ''),
        './issues/issue/vat':('vat', ''),
        './issues/issue/default_net_price':('default_price', ''),
        './issues/issue/net_api_price':('api_price', ''),
        './issues/issue/default_spread':('default_spread', ''),
        './issues/issue/image':('cover', ''),
        "./issues/issue/format{'./type':('format', ''), './file-protection/type':('protection',''), './file-protection/properties':('properties','')}":('format', ''),
       }


    def __init__(self, name=None):
        XMLConnector.__init__(self, name=name)

    def downloadFile(self):
        values = {'api_id': self.config['api_id'],
             'pass': self.config['pass'],
             'xmlType':self.config['xmltype']}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        rsp = urllib2.urlopen(req)
        content = rsp.read()
        if self.backup_dir and not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        filename = os.path.join(self.backup_dir, self.filename)
        open(filename, "wb").write(content)


Base = SqlWrapper.getBaseClass()

class NextoBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)

class NextoBookDescription(GenericBookDescription, Base):
    pass

class NextoAuthor(GenericAuthor, Base):
    pass

class NextoBookPrice(GenericBookPrice, Base):
    pass

class NextoBooksAuthors(GenericBooksAuthors, Base):
    pass

