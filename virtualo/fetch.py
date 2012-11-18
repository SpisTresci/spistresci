#!/usr/bin/env python
import urllib2
import zipfile
import os.path

url = "https://virtualo.pl/data/cennik_full.zip"

def download(url):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    last_modified = meta.getheaders("Last-Modified")[0]
    print "File last modified: " + last_modified
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)

        #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        #status = status + chr(8)*(len(status)+1)
        #print status,

    f.close()


def decompres(zipname):

    zfile = zipfile.ZipFile(zipname)
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)

        if dirname == "":
            dirname = zipname.split(".")[0]

        print "Decompressing " + filename + " on " + dirname
        if not os.path.exists(dirname) and dirname != "":
            os.mkdir(dirname)
        fd = open(dirname + os.sep + name,"w")
        fd.write(zfile.read(name))
        fd.close()


if __name__ == '__main__':

    download(url)
    decompres(os.path.split(url)[1])
