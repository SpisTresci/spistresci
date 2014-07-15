from PyZ3950 import zoom, zmarc
import os

# ***** To run this, please Install PyZ3950: *****
# git clone git://github.com/asl2/PyZ3950.git PyZ3950
# cd PyZ3950
# sudo python setup.py install
#
# ********  PyZ3950 also need ply library: *******
# sudo easy_install ply

class MARCConnector(object):

    def makeConnection(self):
        conn = zoom.Connection (self.url, int(self.port))
        conn.databaseName = self.database_name
        conn.preferredRecordSyntax = self.preferred_record_syntax
        return conn

    def fetchMods(self, query):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        i = 0
        for res in self.conn.search (zoom.Query ('CCL', query)):
            if i % self.XML_FILE_SIZE_LIMIT == 0:
                filename = os.path.join(self.backup_dir, self.filename.replace(".xml", "_%d.xml" % int(i/self.XML_FILE_SIZE_LIMIT)))
                self.fetched_files.append(filename)
                f = open(filename, 'w')
                f.write("<root>\n")

            marc_obj = zmarc.MARC (res.data, strict=0)
            f.write(marc_obj.toMODS() + "\n")
            i = i + 1
            print i

            if i % self.XML_FILE_SIZE_LIMIT == 0:
                f.write("</root>\n")
                f.close()

        else:
            if  i % self.XML_FILE_SIZE_LIMIT != 0:
                f.write("</root>\n")
                f.close()