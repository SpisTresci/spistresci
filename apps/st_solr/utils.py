import urllib
import urllib2
import zipfile
import sys

def unpackZIP(zipname, dst_dir):
    with zipfile.ZipFile(zipname, "r") as z:
        z.extractall(dst_dir)

def downloadFile(url, file_name, progress_bar=True):
    if progress_bar:
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: {0} Bytes: {1}".format(url, file_size)
        print "Saving to %s" % file_name

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            p = float(file_size_dl) / file_size
            status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
            status = status + chr(8)*(len(status)+1)
            sys.stdout.write(status)

        f.close()

    else:
        urllib.urlretrieve (url, file_name)
