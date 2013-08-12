from connectors.generic import GenericConnector
from utils import Enum
import lxml.etree as et
import os
import re
import hashlib

class XMLConnector(GenericConnector):

    xml_tag_dict = {}
    depth = 0

    def get_et(self):
        return et

    def fetchData(self, unpack=True, download=True):
        self.save_time_of_("fetch_start")

        if download:
            self.downloadFile()

        if unpack and self.mode == XMLConnector.BookList_Mode.ZIPPED_XMLS:
            self.fetched_files.extend(
              self.unpackZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif unpack and self.mode == XMLConnector.BookList_Mode.GZIPPED_XMLS:
            self.fetched_files.extend(
              self.unpackGZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif unpack and self.mode == XMLConnector.BookList_Mode.BZIPPED_XMLS:
            self.fetched_files.extend(
              self.unpackBZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif self.mode == XMLConnector.BookList_Mode.SINGLE_XML:
            self.fetched_files.append(os.path.join(self.backup_dir, self.filename))

        self.save_time_of_("fetch_end")

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
        """
        Translate book xml into dictionary used to insert into database
        :param book: book xml root
        :param xml_tag_dict: dictionary of xpaths used to translate
        :return: created dictionary
        """

        if xml_tag_dict is None:
            xml_tag_dict = self.xml_tag_dict

        book_dict = {}
        for (dict_key, xpath) in xml_tag_dict.items():
            (tag, default_0) = xpath
            regex = re.compile("([^{]*)({.*})?")
            recurency = regex.search(tag).groups()
            ntag = recurency[0]
            elems = book.xpath(ntag, namespaces=self.xmls_namespace)
            for elem in elems:
                if recurency[1] != None:
                    self.getDictFromElem(eval(recurency[1]), dict_key, elem, tag, book_dict)
                else:
                    self.getValueFromElem(dict_key, default_0, elem, ntag, book_dict)

            book_dict.setdefault(dict_key, (unicode(default_0) if default_0 != None else None))

            if book_dict[dict_key] != None and len(book_dict[dict_key]) == 1:
                book_dict[dict_key] = book_dict[dict_key][0]

        return book_dict

    def weHaveToGoDeeper(self, root, depth):
        for i in range(int(depth)):
            root = root[0]
        return root

    def getBookList(self, filename):
        root = self.get_et().parse(filename).getroot()
        return list(self.weHaveToGoDeeper(root, self.depth))

    def calculateChecksum(self):
        m = hashlib.md5()
        for file in self.fetched_files:
            with open(file, "r") as f:
                m.update(f.read())

        return m.hexdigest()

    def getDictFromElem(self, xml_tag_dict, new_tag, elem, tag, book_dict):
        if elem != None:
            if book_dict.get(new_tag) == None:
                book_dict[new_tag] = []

            book_dict[new_tag].append(self.makeDict(elem, xml_tag_dict))

    def getValueFromElem(self, new_tag, default_0, elem, tag, book_dict):
        if elem != None:
            if book_dict.get(new_tag) == None:
                book_dict[new_tag] = []

            if "@" in tag.split('/')[-1]:
                # from //path/tag[@attrib='value'] extract (u'attrib', u'value'), and from //path/tag[@attrib] extract (u'attrib', None)
                regex = re.compile("\[?@(\w+)(?:='(.+?)')?\]?")
                atrrib_value = regex.search(tag).groups()

                if atrrib_value[1] == None and isinstance(elem, et._Element):
                    book_dict[new_tag].append(unicode(elem.attrib.get(atrrib_value[0], default_0)))
                elif atrrib_value[1] == None:
                    book_dict[new_tag].append(unicode(elem))
                else:
                    book_dict[new_tag].append(unicode(elem.text if elem.text != "" and elem.text != None else default_0))
            else:
                book_dict[new_tag].append(unicode(elem.text if elem.text != "" and elem.text != None else default_0))

