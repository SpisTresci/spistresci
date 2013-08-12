from connectors.generic import GenericConnector
import os
import codecs
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

class OAIConnector(GenericConnector):

    translate_tag_dict = {}

    def fetchData(self):
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(self.url, registry)
        self.records = []
        i = 0

        for record in client.listRecords(metadataPrefix='oai_dc'):
            record_dic = record[1].getMap()
            self.records.append(record_dic)
            i += 1
            if i == 100:
                print "Downloaded records: " + str(len(self.records))
                i = 0

        if self.backup_dir and not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        filename = os.path.join(self.backup_dir, self.filename)
        f = codecs.open(filename, 'w', 'utf-8')
        f.write(str(self.records))
        f.close()
        self.fetched_files.append(filename)

    def makeDict(self, offer):
        for new_name, (old_name, default) in self.translate_tag_dict.items():
            if offer.get(old_name) != None:
                item = offer.pop(old_name)

                if not isinstance(item, basestring):
                    if isinstance(item, list):
                        if len(item) == 1:
                            offer[new_name] = item[0]
                        elif len(item) == 0:
                            offer[new_name] = default
                        else:
                            offer[new_name] = item
                    else:
                        raise Exception("Unexpected data format! Connector " + self.name)
                else:
                    offer[new_name] = item

        return offer

    def getBookList(self, filename):
        return self.records
