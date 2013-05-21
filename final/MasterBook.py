import final
from sqlwrapper import *
import utils
Base = SqlWrapper.getBaseClass()

class MasterBook(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    title = Column(Unicode(512))  # , unique=True)
    #TODO: remove
    #title_simplified = Column(STUnicode10(512))  # , unique=True)

    format_mobi = Column(Boolean)
    format_epub = Column(Boolean)
    format_pdf = Column(Boolean)
    format_mp3 = Column(Boolean)
    format_cd = Column(Boolean)

    isbns = relationship("MasterISBN", lazy = 'joined', secondary = final.master_books_master_isbns, backref = "masterBook")
    authors = relationship("MasterAuthor", lazy = 'joined', secondary = final.master_books_master_authors, backref = "masterBook")
    miniBooks = relationship("MiniBook", backref = backref("masterBook", uselist = False, lazy = 'joined'))
    words = relationship("TitleWord", secondary = final.master_books_title_words, backref = "masterBook")

    def __init__(self, mini_book):
        if not isinstance(mini_book, final.MiniBook):
            raise "MasterBook can be only initialize by MiniBook"

        self.title = mini_book.title
        #TODO: remove
        #self.title_simplified = utils.SimilarityCalculator.simplify(mini_book.title)

        for isbn in mini_book.isbns:
            self.isbns.append(isbn.masterISBN)

        for author in mini_book.authors:
            self.authors.append(author.masterAuthor)

    def addMiniBook(self, new_miniBook):
        if not any(new_miniBook.bookstore == miniBook.bookstore and \
                   new_miniBook.bookstore_boook_id == miniBook.bookstore_boook_id for miniBook in self.miniBooks):

            self.miniBooks.append(new_miniBook)

            for key in vars(new_miniBook).keys():
                if key.startswith("format_"):
                    value = getattr(new_miniBook, key)
                    if value == True:
                        setattr(self, key, value)
