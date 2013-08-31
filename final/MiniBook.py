import final
import utils
from sqlwrapper import *
from sqlalchemy.orm import lazyload
Base = SqlWrapper.getBaseClass()

class MiniBook(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    master_id = Column(Integer, ForeignKey('MasterBook.id'))

    title = Column(Unicode(512), nullable = False)
    url = Column(Unicode(512), nullable = False)
    cover = Column(Unicode(512), nullable = False)

    bookstore = Column(Unicode(16), nullable = False)
    bookstore_book_id = Column(Integer, nullable = False)

    price = Column(Integer, nullable = False)
    isbns = relationship("MiniISBN", secondary = final.mini_books_mini_isbns, backref = "mini_book")
    authors = relationship("MiniAuthor", secondary = final.mini_books_mini_authors, backref = "mini_book")

    @declared_attr
    def words(cls):
        if SqlWrapper.isEgoistStrategyOn():
            return relationship("TitleWord", secondary = final.mini_books_title_words, backref = backref("mini_book", lazy = "joined"))
        else:
            return relationship("TitleWord", secondary = final.mini_books_title_words, backref = backref("mini_book", lazy = "joined", cascade = ""))


    #supported_formats = ['cd', 'cd-mp3', 'dvd', 'epub', 'fb2', 'ks', 'mobi', 'mp3', 'pdf', 'txt', 'xml']

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

    def splitTitle(self, title):
        title = utils.Str.removePunctuation(title)
        return [word.strip() for word in title.split()]

    def __init__(self, session, specific_book):
        self.title = specific_book.title
        self.price = specific_book.price
        self.url = specific_book.url
        self.cover = specific_book.cover

        self.bookstore = specific_book.__tablename__[:-len("Book")]
        self.bookstore_book_id = specific_book.id

        vars_all = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
        formats = [key for key in vars_all if key.startswith("format_")]
        specific_formats = [f.name for f in specific_book.formats]
        for f in formats:
            setattr(self, f, f.replace("format_", "") in specific_formats)

        authors = specific_book.authors
        for author in authors:
            ma = final.MiniAuthor(author)
            self.authors.append(ma)

        isbns = specific_book.isbns
        for isbn in isbns:
            mi = final.MiniISBN(isbn)
            self.isbns.append(mi)

        self.splited_and_simplified_title = [utils.Str.simplify(word) for word in self.splitTitle(self.title)]

        for word in self.splited_and_simplified_title:
            titleWord = final.TitleWord.get_or_create(session, word)
            self.words.append(titleWord)

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
                master_Book = final.MasterBook()
                master_Book.addMiniBook(mini_book)
            elif len(equal_master_Books) == 1:
                master_Book = equal_master_Books[0]
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
                master_Book.addMiniBook(mini_book)

            session.add(master_Book)
            #session.commit()

        MiniBook.to_normalize = []

    def update(self, session, specific_book):
        #TODO: implement update of other fields
        if self.price != specific_book.price:
            self.price = specific_book.price

    @staticmethod
    def getMasterBookCandidates(session, mini_book):
        masters = set()
        mini_book_id = mini_book.id
        #words = session.query(final.TitleWord).options(lazyload('mini_book')).filter(final.TitleWord.mini_book.any()  id = mini_book_id).all()

        words = mini_book.words

        for titleWord in words:
            for titleWord in titleWord.soundex.words:
                for miniBook in titleWord.mini_book:
                    if miniBook.id != mini_book.id and miniBook.masterBook != None:
                        masters.add(miniBook.masterBook)
        return list(masters)
