from connectors.generic import XMLConnector

import os
import re
from xml.dom import minidom

class Virtualo(XMLConnector):

    def __init__(self, name=None):
        XMLConnector.__init__(self, name=name)

    def parse(self):

        i = 1

        while True:
            filename = 'VirtualoProducts' + str(i) + '.xml'
            filename = os.path.join(self.unpack_dir, filename)
            if not os.path.exists(filename):
                break

            DOMTree = minidom.parse(filename)

            products = DOMTree.childNodes.item(0).childNodes

            self.logger.debug('Parsing %s' % os.path.split(filename)[1])

            for product in products:
                title = self.getTagValue(product, 'title')
                format = self.getTagValue(product, 'format')
                security = self.getTagValue(product, 'security', 'brak')
                price = self.getTagValue(product, 'price')
                isbn = self.getTagValue(product, 'isbn')
                coverId = self.getTagValue(product, 'coverId')
                authors = self.getTagValue(product, 'authors')
                #print authors
                #splitObj = re.split(', ', authors)
                #if len(splitObj) != 1:
                #    print authors

                url = self.getTagValue(product, 'url')
                description = self.getTagExpliciteValue(product, 'description')
                rating = self.getTagValue(product, 'rating')

                matchObj = re.match(r'.*/i(\d*)/', url)
                id = int(matchObj.group(1))


                #format_tag = product.getElementsByTagName('format')[0]
                #format = ""
                #if format_tag.firstChild != None:
                #      format = format_tag.firstChild.nodeValue


                #format = product.getElementsByTagName('format')[0].firstChild.nodeValue

                #security = product.getElementsByTagName('security')[0].firstChild.nodeValue

            self.logger.debug('File %s parsed' % os.path.split(filename)[1])
            self.logger.debug('Virtualo, read %d products' % len(products))
            i = i + 1

        pass


