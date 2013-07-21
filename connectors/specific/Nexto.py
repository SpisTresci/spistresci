from connectors.generic import XMLConnector
import os
from sqlwrapper import *
from connectors.generic import GenericBook
import urllib, urllib2

class Nexto(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('./id', None),
        'isbns': ('./isbn', ''),
        'lang_short': ('./language', ''),
        'description': ('./body', ''),
        'title': ('./title', ''),
        'publisher': ('./publisher', ''),
        'manufacturer_id': ('./manufacturer_id', ''),
        'product_code': ('./product_code', ''),

        'category_id': ('./category_refs/id', ''),

        'issue_id': ('./issues/issue/issue_id', ''),
        'authors': ('./issues/issue/author', ''),
        'gross_price': ('./issues/issue/gross_nexto_price', ''),
        'vat': ('./issues/issue/vat', ''),
        'default_price': ('./issues/issue/default_net_price', ''),
        'api_price': ('./issues/issue/net_api_price', ''),
        'default_spread': ('./issues/issue/default_spread', ''),
        'cover': ('./issues/issue/image', ''),
        'formats': ("./issues/issue/format{'format': ('./type', ''), 'protection': ('./file-protection/type', ''), 'properties': ('./file-protection/properties', '')}", ''),
       }

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
    id = Column(Integer, primary_key = True)

#TODO: define whole tables for Nexto

