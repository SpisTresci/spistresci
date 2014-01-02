# -*- coding: utf-8 -*-
import final
from sqlwrapper import *
from final.Base.BaseBook import *
from final.Base.BaseMaster import *

Base = SqlWrapper.getBaseClass()

class MasterBook(BaseMaster, BaseBook, Base):
    isbn = relationship("MasterISBN", uselist = False, backref = backref("masterBook", uselist = False))
    authors = relationship("MasterAuthor", secondary = final.master_books_master_authors, backref = "master")
    minis = relationship("MiniBook", backref = backref("master", uselist = False))
    words = relationship("TitleWord", secondary = final.master_books_title_words, backref = "masterBook")

    active = Column(Boolean, default=True)

    def __init__(self, mini_book = None):
        if mini_book:
            raise "not supported any more. Use empty constructor, and next addMini"

    def addMini(self, new_miniBook):
        if not isinstance(new_miniBook, final.MiniBook):
            raise "MasterBook can be only initialize by MiniBook"

        if len(self.minis) == 0:
            self.title = new_miniBook.title
            self.description = new_miniBook.description
            self.price = new_miniBook.price
            self.cover = new_miniBook.cover

        if not any(new_miniBook.bookstore == miniBook.bookstore and \
                   new_miniBook.bookstore_book_id == miniBook.bookstore_book_id for miniBook in self.minis):

            self.minis.append(new_miniBook)

            for isbn in new_miniBook.isbns:
                try:
                    if isbn not in self.isbn.minis:
                        self.isbn.minis.append(isbn)
                except AttributeError:  #not all books has isbns
                    self.isbn = isbn.master

            for author in new_miniBook.authors:
                if author.master not in self.authors:
                    self.authors.append(author.master)

            vars_all = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
            formats = [key for key in vars_all if key.startswith("format_")]

            for f in formats:
                #here can not be just setattr(self, f, getattr(new_miniBook, f, False)), because False from new book could override old True value
                if getattr(new_miniBook, f, False):
                    setattr(self, f, True)

    def removeMini(self, mini_book):
        for isbn in mini_book.isbns:
            if isbn.master == self.isbn:
                self.isbn = None

        for author in mini_book.authors:
            if author.master in self.authors:
                self.authors.remove(author.master)

    def getMasterBooksCandidatesByISBN(self, session):
        c = []
        for mini in self.minis:
            c += mini.getMasterBooksCandidatesByISBN(session)

    def mergeWith(self, masterbooks):
        for master in masterbooks:
            for mini in master.minis:
                master.removeMini(mini)
                self.addMini(mini)
            del master.minis[:]

            for author in self.authors:
                author.mergeWith(master.authors)

    def __repr__(self):
        repr = "[%d](%s) %s" % (self.id, ", ".join([str(mini.id) for mini in self.minis]), self.title)

        vars_all = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
        formats = [key for key in vars_all if key.startswith("format_")]
        repr += " (" + ", ".join([f.replace("format_", "") for f in formats if getattr(self, f)]) + ")"
        repr += " <"  + self.isbn.__repr__() + ">"

        return repr


##########################################3

    def cmp(self, other):
        """
         1. Szybkie odrzucenie, badź perfekcyjne dopasowanie
         2. 1-n/n-1 (odrzucic)
         3. 1-n/n-1 (całość)
         4. liniowe potwierdzenie
         5. Kazdy z każdym

        """

        cached = self.cache.get(self, other)

        if cached:
            return cached.result, cached.merged
        else:
            r = self.Result()

            #szybkie odrzucenie
            r.addRatio(cmp(self.title, other.title))
            r.add(cmp(self.isbn, other.isbn))
            r.addRatio(cmp_lists(self.authors, other.authors))

            if r.result() < self.instant_abort_threshold:
                return self.cache.set(self, other, (r.result(), False))

            elif r.result() >= self.instant_accept_threshold:
                merge(self, other, None)
                return self.cache.set(self, other, (r.result(), True))

            else:

                r = self.Result()
                for master, minis in [(self, other.minis), (other, self.minis)]:
                    for mini in minis:
                        r.addRatio(cmp(master.title, mini.title))

                if r.result() < self.second_abort_threshold:
                    return self.cache.set(self, other, (r.result(), False))

                for master, minis in [(self, other.minis), (other, self.minis)]:
                    for mini in minis:
                        r.addRatio(cmp_lists([master.isbn] if master.isbn else [], mini.isbns))
                        r.addRatio(cmp_lists(master.authors, mini.authors))

                if r.result() >= self.second_accept_threshold:
                    merge(self, other, None)
                    return self.cache.set(self, other, (r.result(), True))
                else:
                    return self.cache.set(self, other, (r.result(), False))

    instant_abort_threshold = 0.15
    second_abort_threshold = 0.25

    instant_accept_threshold = 0.95
    second_accept_threshold = 0.85

    merged = 0

    def merge(self, other, result):
        MasterBook.merged += 1
        print "MasterBook::merge - " + str(MasterBook.merged)
        for mini in other.minis:
            other.removeMini(mini)
            other.active = False
            self.addMini(mini)
            self.active = True

