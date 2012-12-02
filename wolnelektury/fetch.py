#!/usr/bin/env python
import urllib2
import json
url = 'http://wolnelektury.pl/api/books/'

def main():
    page = urllib2.urlopen(url)
    books_page = page.read()
    book_list = json.loads(books_page)
    for book in book_list:
        book_page = urllib2.urlopen(book[u'href'])
        book_details = json.loads(book_page)
        book = dict((n,book.get(n,0),book_details.get(n,0)) for n in set(book)|set(book_details))

#    print books;


    


if __name__ == '__main__':
    main()

