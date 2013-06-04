from connectors.generic import GenericConnector
from utils import Enum
import lxml.etree as et
import os
import re

class XMLConnector(GenericConnector):

    xml_tag_dict = {}
    depth = 0
    skip_offers = 0

    def __init__(self, name=None, limit_books=0):
        GenericConnector.__init__(self, name=name)
        self.limit_books = limit_books

    def get_et(self):
        return et

    def fetchData(self, unpack=True):
        self.downloadFile()
        if unpack and self.mode == XMLConnector.BookList_Mode.ZIPPED_XMLS:
            self.fetched_files.extend(
              self.unpackZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif unpack and self.mode == XMLConnector.BookList_Mode.GZIPPED_XMLS:
            self.fetched_files.extend(
              self.unpackGZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif self.mode == XMLConnector.BookList_Mode.SINGLE_XML:
            self.fetched_files.append(os.path.join(self.backup_dir, self.filename))

    def getTagValue(self, product, tagName, default=""):
        tag = product.getElementsByTagName(tagName)[0]
        value_of_tag = default
        if tag.firstChild != None:
            value_of_tag = tag.firstChild.nodeValue
        return value_of_tag

    def getTagExpliciteValue(self, product, tagName, default=""):

        tag = product.getElementsByTagName(tagName)[0]
        value_of_tag = default
        if tag.firstChild != None:
            value_of_tag = tag.toxml()
        return value_of_tag[len(('<' + tagName + '>')):-len(('</' + tagName + '>'))]

    xmls_namespace = ""

    def makeDict(self, book, xml_tag_dict=None):
        if xml_tag_dict == None:
            xml_tag_dict = self.xml_tag_dict

        book_dict = {}
        for tag in xml_tag_dict.keys():
            regex = re.compile("([^{]*)({.*})?")
            recurency = regex.search(tag).groups()
            ntag = recurency[0]

            elems = book.xpath(ntag, namespaces=self.xmls_namespace)
            for elem in elems:
                if recurency[1] != None:
                    self.getDictFromElem(eval(recurency[1]), xml_tag_dict[tag][0], elem, tag, book_dict)
                else:
                    self.getValueFromElem(xml_tag_dict, elem, ntag, book_dict)

            t = xml_tag_dict[tag][0]

            if book_dict.get(t) == None:
                book_dict[t] = unicode((xml_tag_dict[tag])[1]) if (xml_tag_dict[tag])[1] != None else (xml_tag_dict[tag])[1];
            elif len(book_dict[t]) == 1:
                book_dict[t] = book_dict[t][0]


        return book_dict

    def weHaveToGoDeeper(self, root, depth):
        for i in range(int(depth)):
            root = root[0]
        return root

    def parse(self):
        self.before_parse()
        book_number = 0
        for filename in self.fetched_files:
            root = self.get_et().parse(filename).getroot()
            offers = list(self.weHaveToGoDeeper(root, self.depth))
            for offer in offers:
                book_number += 1
                if book_number < self.skip_offers + 1:
                    continue
                elif self.limit_books and book_number > self.limit_books:
                    break
                dic = self.makeDict(offer)
                #comment out when creating connector
                self.adjust_parse(dic)
                self.validate(dic)
                #uncomment when creating connector
                #self.measureLenghtDict(dic)
                #print dic
                #comment out when creating connector
                self.add_record(dic)

        self.after_parse()
        #uncomment when creating connector
        #print self.max_len
        #print self.max_len_entry

    def getDictFromElem(self, xml_tag_dict, new_tag, elem, tag, book_dict):
        if elem != None:
            if book_dict.get(new_tag) == None:
                book_dict[new_tag] = []

            book_dict[new_tag].append(self.makeDict(elem, xml_tag_dict))

    def getValueFromElem(self, xml_tag_dict, elem, tag, book_dict):
        if elem != None:
            new_tag = (xml_tag_dict[tag])[0]
            if book_dict.get(new_tag) == None:
                book_dict[new_tag] = []

            if "@" in tag.split('/')[-1]:
                # from //path/tag[@attrib='value'] extract (u'attrib', u'value'), and from //path/tag[@attrib] extract (u'attrib', None)
                regex = re.compile("\[?@(\w+)(?:='(.+?)')?\]?")
                atrrib_value = regex.search(tag).groups()

                if atrrib_value[1] == None and isinstance(elem, et._Element):
                    book_dict[new_tag].append(unicode(elem.attrib.get(atrrib_value[0], (xml_tag_dict[tag])[1])))
                elif atrrib_value[1] == None:
                    book_dict[new_tag].append(unicode(elem))
                else:
                    book_dict[new_tag].append(unicode(elem.text if elem.text != "" and elem.text != None else (xml_tag_dict[tag])[1]))
            else:
                book_dict[new_tag].append(unicode(elem.text if elem.text != "" and elem.text != None else (xml_tag_dict[tag])[1]))

