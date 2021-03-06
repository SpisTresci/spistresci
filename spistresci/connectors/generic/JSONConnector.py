from spistresci.connectors.generic import GenericConnector
from spistresci.connectors.generic import WrongConnectorModeException
from spistresci.connectors.utils.compatibility import json
import os

class JSONConnector(GenericConnector):

    tag_dict = {}

    def makeDict(self, book):
        dic = {}
        for item in self.tag_dict.items():
            (org_key, (key, default))  = item
            dic[key] = book.get(org_key, default)

        return dic

    def fetchData(self, unpack=True):
        self.save_time_of_("fetch_start")
        self.downloadFile()
        #TODO: this definatelly should not be here ..... or... let's not use 'definatelly' here
        if GenericConnector.BookList_Mode.to_str(self.mode).endswith('XML') or GenericConnector.BookList_Mode.to_str(self.mode).endswith('XMLS'):
            raise WrongConnectorModeException('Incorrect mode %s for connector type %s' % 
            (GenericConnector.BookList_Mode.to_str(self.mode), self.__class__.__name__))
        elif unpack and self.mode == GenericConnector.BookList_Mode.ZIPPED_JSON:
            self.fetched_files.extend(
              self.unpackZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif unpack and self.mode == GenericConnector.BookList_Mode.GZIPPED_JSON:
            self.fetched_files.extend(
              self.unpackGZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif self.mode == GenericConnector.BookList_Mode.SINGLE_JSON:
            self.fetched_files.append(os.path.join(self.backup_dir, self.filename))

        self.save_time_of_("fetch_end")

    def getBookList(self, filename):
        with open(filename, 'rU') as json_file:
            book_list = json.load(json_file)
        return book_list

