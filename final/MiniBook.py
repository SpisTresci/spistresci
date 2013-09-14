import final
import utils
from sqlwrapper import *
from final.Base.BaseBook import *
from final.Base.BaseMini import *

Base = SqlWrapper.getBaseClass()

class MiniBook(BaseMini, BaseBook, Base):
    master_id = Column(Integer, ForeignKey('MasterBook.id'))
    #master by backref

    url = Column(Unicode(512), nullable = False)
    bookstore = Column(Unicode(16), nullable = False)
    bookstore_book_id = Column(Integer, nullable = False)
    book_type_id = Column(Integer, ForeignKey('BookType.id'))
    book_type = relationship("BookType", uselist=False)

    isbns = relationship("MiniISBN", backref = backref("mini_book", uselist = False))          #secondary = final.mini_books_mini_isbns, backref = "mini_book")
    authors = relationship("MiniAuthor", secondary = final.mini_books_mini_authors, backref = "mini_book")

    @declared_attr
    def words(cls):
        if SqlWrapper.isEgoistStrategyOn():
            return relationship("TitleWord", backref = backref("mini_book"))
        else:
            return relationship("TitleWord", backref = backref("mini_book", cascade = ""))

    def splitTitle(self, title):
        title = utils.Str.removePunctuation(title)
        return [word.strip() for word in title.split()]

    def __init__(self, session, specific_book):
        specific_book.mini_book = self

        self.title = specific_book.title
        self.price = specific_book.price
        self.url = specific_book.url
        self.cover = specific_book.cover

        self.bookstore = specific_book.__tablename__[:-len("Book")]
        self.bookstore_book_id = specific_book.id
        self.book_type = specific_book.book_type
        self.description = specific_book.description

        vars_all = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
        formats = [key for key in vars_all if key.startswith("format_")]
        specific_formats = [f.name for f in specific_book.formats]
        for f in formats:
            setattr(self, f, f.replace("format_", "") in specific_formats)

        authors = specific_book.authors
        for author in authors:
            ma = final.MiniAuthor(session, author)
            self.authors.append(ma)

        isbns = specific_book.isbns
        for isbn in isbns:
            mi = final.MiniISBN(session, isbn)
            self.isbns.append(mi)

        self.splited_and_simplified_title = [utils.Str.simplify(word) for word in self.splitTitle(self.title)]

        for word in self.splited_and_simplified_title:
            self.words.append(final.TitleWord(word))

        master_Book = final.MasterBook()
        master_Book.addMini(self)
        session.add(master_Book)

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
                    if miniBook.id != mini_book.id and miniBook.master != None:
                        masters.add(miniBook.master)
        return list(masters)

    def __repr__(self):
        repr = "(%d)[%d] %s" % (self.id, self.master_id, self.title)

        vars_all = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
        formats = [key for key in vars_all if key.startswith("format_")]
        repr += " (" + ", ".join([f.replace("format_", "") for f in formats if getattr(self, f)]) + ")"
        repr += " <" + ", ".join([isbn.__repr__() for isbn in self.isbns]) + ">"

        return repr

    def supported(self):
        from models import BookType
        return  self.book_type_id != BookType.BookType.PRESS

    def getMasterBooksCandidatesByISBN(self, session, master_isbn, inner_merge = False):
        if not self.supported():
            return []

        isbns = set()
        cores = []
        raws = []
        for mini_isbn in self.isbns:
            cores.append(mini_isbn.core)
            raws.append(mini_isbn.raw)

        condition = final.MiniISBN.raw.in_(raws)

        if len(cores) > 0:
            condition = or_(condition, final.MiniISBN.core.in_(cores))

        if inner_merge:
            condition = and_(condition, final.MiniISBN.bookstore == self.bookstore)

        if master_isbn:
            condition = and_(condition, final.MiniISBN.master_id != master_isbn.id)

        isbns.update(session.query(final.MiniISBN).filter(condition).all())

        master_isbns = set()
        for mini_isbn in list(isbns):
            master_isbns.add(mini_isbn.master)

        master_books = []
        for mini_isbn in isbns:
            master_books.append(mini_isbn.master.masterBook)

        return master_books


    def getMasterBooksCandidatesByTitle(self, session):
        if not self.supported():
            return []

        minis = session.query(final.MiniBook).filter(final.MiniBook.title == self.title,
                                             final.MiniBook.master_id != self.master_id
                                             ).all()

        return [mini.master for mini in minis]

################################################################

    def cmp(self, other):
        cached = self.cache.get(self, other)

        if cached:
            return cached.result, cached.merged
        else:
            r = self.Result()

            r.addRatio(cmp(self.title, other.title))
            r.addRatio(cmp_lists(self.isbns, other.isbns))
            r.addRatio(cmp_lists(self.authors, other.authors))

            return self.cache.set(self, other, merge(self, other, r.result()))

    accept_threshold = 0.9

    def getCandidates(self, session, inner):
        pass

    def getCandidatesByISBN(self, session, inner):
        if len(self.isbns)  == 0:
            return []

        ids, cores, raws, master_isbn_ids = zip(*[(isbn.id, isbn.core, isbn.raw, isbn.master_id) for isbn in self.isbns])

        condition = final.MiniISBN.raw.in_(raws)
        if len(cores) > 0: condition = or_(condition, final.MiniISBN.core.in_(cores))
        if inner:    condition = and_(condition, final.MiniISBN.bookstore == self.bookstore)
        condition = and_(condition, not_(final.MiniISBN.master_id.in_(master_isbn_ids)))
        condition = and_(condition, not_(final.MiniISBN.id.in_(ids)))

        candidates_isbns = session.query(final.MiniISBN).filter(condition).all()

        minis = [isbn.mini_book for isbn in candidates_isbns]

        return minis

    def getCandidatesByTitleWord(self, session, inner):

        if len(self.words) == 0:
            return []

        word_tpls = [(title_word.id, title_word.word, title_word.soundex) for title_word in self.words if not title_word.stopword]
        if len(word_tpls) == 0:
            word_tpls += [(title_word.id, title_word.word, title_word.soundex) for title_word in self.words if title_word.stopword]

        ids, words, soundex = zip(*word_tpls)

        condition = final.TitleWord.word.in_(words)
        condition = and_(condition, not_(final.TitleWord.id.in_(ids)))
        candidates_title_words = session.query(final.TitleWord).filter(condition).all()

        #TODO: check inpact and apply if it helps
        #filter outs candidates with this same master.
        #condition = and_(condition, not_(final.TitleWord.mini_book.master_id == self.master))
        #.options(joinedload('mini_book')

        minis = list(set([title_word.mini_book for title_word in candidates_title_words]))

        return minis