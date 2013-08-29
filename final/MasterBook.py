import final
from sqlwrapper import *
import utils
Base = SqlWrapper.getBaseClass()

class MasterBook(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    title = Column(Unicode(512))

    #supported_formats = ['cd', 'cd_mp3', 'dvd', 'epub', 'fb2', 'ks', 'mobi', 'mp3', 'pdf', 'txt', 'xml']

    format_cd = Column(Boolean, default=False)
    format_cd_mp3 = Column(Boolean, default=False)
    format_dvd = Column(Boolean, default=False)
    format_epub = Column(Boolean, default=False)
    format_fb2 = Column(Boolean, default=False)
    format_ks = Column(Boolean, default=False)
    format_mobi = Column(Boolean, default=False)
    format_mp3 = Column(Boolean, default=False)
    format_pdf = Column(Boolean, default=False)
    format_txt = Column(Boolean, default=False)
    format_xml = Column(Boolean, default=False)



    isbns = relationship("MasterISBN", lazy = 'joined', secondary = final.master_books_master_isbns, backref = "masterBook")
    authors = relationship("MasterAuthor", lazy = 'joined', secondary = final.master_books_master_authors, backref = "masterBook")
    miniBooks = relationship("MiniBook", backref = backref("masterBook", uselist = False, lazy = 'joined'))
    words = relationship("TitleWord", secondary = final.master_books_title_words, backref = "masterBook")

    def __init__(self, mini_book = None):
        if mini_book:
            raise "not supported any more. Use empty constructor, and next addMiniBook"

    def addMiniBook(self, new_miniBook):
        if not isinstance(new_miniBook, final.MiniBook):
            raise "MasterBook can be only initialize by MiniBook"

        if len(self.miniBooks) == 0:
            self.title = new_miniBook.title

        if not any(new_miniBook.bookstore == miniBook.bookstore and \
                   new_miniBook.bookstore_book_id == miniBook.bookstore_book_id for miniBook in self.miniBooks):

            self.miniBooks.append(new_miniBook)

            for isbn in new_miniBook.isbns:
                self.isbns.append(isbn.masterISBN)

            for author in new_miniBook.authors:
                self.authors.append(author.masterAuthor)

            vars_all = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
            formats = [key for key in vars_all if key.startswith("format_")]

            for f in formats:
                #here can not be just setattr(self, f, getattr(new_miniBook, f, False)), because False from new book could override old True value
                if getattr(new_miniBook, f, False):
                    setattr(self, f, True)
