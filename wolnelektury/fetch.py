#!/usr/bin/env python
import urllib2
import json
url = 'http://wolnelektury.pl/api/books/'

def main():
    socket = urllib2.urlopen(url)
    books_page = socket.read()
    book_list = json.loads(books_page)
    for book in book_list:
        book_socket = urllib2.urlopen(book[u'href'])
        book_page =book_socket.read()
        book_socket.close()
        print book_page;
        book_details = json.loads(book_page)
        (book.setdefault(n,book_details.get(n,0)) for n in set(book_details))

    print books;


if __name__ == '__main__':
    main()
