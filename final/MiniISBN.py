import final
import utils
from Comparable import *
from final.Base.BaseISBN import *
from final.Base.BaseMini import *

Base = SqlWrapper.getBaseClass()

class MiniISBN(BaseMini, BaseISBN, Base):
    master_id = Column(Integer, ForeignKey('MasterISBN.id'))
    #master by backref

    mini_book_id = Column(Integer, ForeignKey('MiniBook.id'))

    bookstore = Column(Unicode(16))
    bookstore_isbn_id = Column(Integer)

    def __init__(self, session, specific_isbn):
        self.session = session
        self.raw = specific_isbn.raw
        #self.raw_simplified = utils.SimilarityCalculator.simplify(specific_isbn.raw)

        self.core = specific_isbn.core
        self.isbn10 = specific_isbn.isbn10
        self.isbn13 = specific_isbn.isbn13
        self.valid = specific_isbn.valid

        self.bookstore = specific_isbn.__tablename__[:-len("ISBN")]
        self.bookstore_isbn_id = specific_isbn.id

        master_ISBN = final.MasterISBN(self)
        master_ISBN.minis.append(self)
        self.session.add(master_ISBN)

    @staticmethod
    def getMasterISBNCandidates(session, mini_isbn):
        r = []

        r.append(session.query(final.MasterISBN).filter(final.MasterISBN.core == mini_isbn.core).all())
        #r.append(session.query(final.MasterISBN).filter(final.MasterISBN.raw_simplified.isSimilar(utils.SimilarityCalculator.simplify(mini_isbn.raw_simplified))).all())

        #union on all lists in the list 'r'
        result = []
        for list_elem in r:
            result = list(set(result) | set(list_elem))

        return result

    def __repr__(self):
        return "(%d)[%d]%s" % (self.id, self.master_id, self.raw)
