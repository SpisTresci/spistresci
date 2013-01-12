from generic import XMLConnector
from xml.etree import ElementTree as et
import os
import urllib, urllib2


class Nexto(XMLConnector):



    def __init__(self):
        XMLConnector.__init__(self)
        
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
        filename=os.path.join(self.backup_dir, self.filename)

        open(filename, "wb").write(content)
        
    def parse(self):
                 
        filename  = os.path.join(self.unpack_dir,self.unpack_file)
        if not os.path.exists(filename):
             raise IOError('%s connector, missing xml file %s'%(self.my_name(),filename))

        root = et.parse(filename).getroot()
        
        for product in root:
            id = product.findtext('id','')
            isbn = product.findtext('isbn','')
            language = product.findtext('language','')
            description = product.findtext('body','')
            title = product.findtext('title','')
            publisher = product.findtext('publisher','')
            manufacturer_id = product.findtext('manufacturer_id','')

            print "Tytul: ",title
            print "ID: ",id
            print "Opis: ",description
        
def main():
    
        nexto = Nexto()
        
        nexto.fetchData()
        nexto.parse()
        #konektor.update()
        

if __name__ == '__main__':
    main()
