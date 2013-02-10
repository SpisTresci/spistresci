#!/usr/bin/env python
import urllib2
try:
    import json
except ImportError:
    import simplejson as json
url = 'http://wolnelektury.pl/api/books/'

def fetch():
    socket = urllib2.urlopen(url)
    books_page = socket.read()
    book_list = json.loads(books_page)
    for book in book_list:
        book_socket = urllib2.urlopen(book[u'href'])
        book_page =book_socket.read()
        book_socket.close()
        book_details = json.loads(book_page)
        book.update(book_details)

    print book_list
if __name__ == '__main__':
    fetch()
