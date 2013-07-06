import final
from sqlwrapper import *
import utils
Base = SqlWrapper.getBaseClass()

class MasterBook(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    title = Column(Unicode(512))

    format_mobi = Column(Boolean)
    format_epub = Column(Boolean)
    format_pdf = Column(Boolean)
    format_mp3 = Column(Boolean)
    format_cd = Column(Boolean)

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
                   new_miniBook.bookstore_boook_id == miniBook.bookstore_boook_id for miniBook in self.miniBooks):

            self.miniBooks.append(new_miniBook)

            for isbn in new_miniBook.isbns:
                self.isbns.append(isbn.masterISBN)

            for author in new_miniBook.authors:
                self.authors.append(author.masterAuthor)

            vars_all = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
            formats = [key for key in vars_all if key.startswith("format_")]

            for f in formats:
                value = getattr(new_miniBook, f, False)
                setattr(self, f, value if value else False)
