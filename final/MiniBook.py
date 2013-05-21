import final
import utils
from sqlwrapper import *
from sqlalchemy.orm import lazyload
Base = SqlWrapper.getBaseClass()

class MiniBook(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    master_id = Column(Integer, ForeignKey('MasterBook.id'))

    title = Column(Unicode(512))

    bookstore = Column(Unicode(16))
    bookstore_boook_id = Column(Integer)

    price = Column(Integer)
    isbns = relationship("MiniISBN", secondary = final.mini_books_mini_isbns, backref = "mini_book")
    authors = relationship("MiniAuthor", secondary = final.mini_books_mini_authors, backref = "mini_book")
    words = relationship("TitleWord", secondary = final.mini_books_title_words, backref = backref("mini_book", lazy = "joined"))

    format_mobi = Column(Boolean)
    format_epub = Column(Boolean)
    format_pdf = Column(Boolean)
    format_mp3 = Column(Boolean)
    format_cd = Column(Boolean)

    def splitTitle(self, title):
        title = utils.Str.removePunctuation(title)
        return [word.strip() for word in title.split()]

    def __init__(self, session, specific_book):
        self.title = specific_book.title
        self.price = specific_book.price

        self.splited_and_simplified_title = [utils.Str.simplify(word) for word in self.splitTitle(self.title)]

        for word in self.splited_and_simplified_title:
            titleWord = final.TitleWord.get_or_create(session, word)
            self.words.append(titleWord)

        self.bookstore = specific_book.__tablename__[:-len("Book")]
        self.bookstore_boook_id = specific_book.id

        formats = specific_book.formats
        for format in formats:
            setattr(self, "format_" + format.name, True)

        authors = specific_book.authors
        for author in authors:
            ma = final.MiniAuthor(author)
            self.authors.append(ma)

        isbns = specific_book.isbns
        for isbn in isbns:
            mi = final.MiniISBN(isbn)
            self.isbns.append(mi)

    to_normalize = []

    @staticmethod
    def normalize(session):
        final.MiniAuthor.normalize(session)
        final.MiniISBN.normalize(session)

        for mini_book in MiniBook.to_normalize:
            #print "To normalize: " + mini_book.title

            master_Books = MiniBook.getMasterBookCandidates(session, mini_book)

            equal_master_Books = []

            for master_Book in master_Books:
                if utils.SimilarityCalculator.eq_books(mini_book, master_Book):
                    equal_master_Books.append(master_Book)

            master_Book = None

            if len(equal_master_Books) == 0:
                #create masterISBN from miniBook
                master_Book = final.MasterBook(mini_book)
                #master_Book.miniBooks.append(mini_book)
                master_Book.addMiniBook(mini_book)
            elif len(equal_master_Books) == 1:
                #add miniBook to masterISBN
                master_Book = equal_master_Books[0]
                #master_Book.miniBooks.append(mini_book)
                master_Book.addMiniBook(mini_book)
            elif len(equal_master_Books) > 1:
                #master should be probably merged
                ratio = 0.0
                best_match = None
                for em in equal_master_Books:
                    r = utils.SimilarityCalculator.mini_master_books_ratio(mini_book, em)
                    if r > ratio:
                        best_match = em
                        ratio = r
                master_Book = best_match
                #master_Book.miniBooks.append(mini_book)
                master_Book.addMiniBook(mini_book)

            session.add(master_Book)
            #session.commit()

        MiniBook.to_normalize = []


    @staticmethod
    def getMasterBookCandidates(session, mini_book):
        masters = set()
        mini_book_id = mini_book.id
        words = session.query(final.TitleWord).options(lazyload('mini_book')).filter_by(id = mini_book_id).all()
        for titleWord in words:
            for titleWord in titleWord.soundex.words:
                for miniBook in titleWord.mini_book:
                    if miniBook.id != mini_book.id:
                        masters.add(miniBook.masterBook)
        return list(masters)
