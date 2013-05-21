import final
import utils
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class MiniISBN(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    master_id = Column(Integer, ForeignKey('MasterISBN.id'))

    raw = Column(Unicode(50))
    #raw_simplified = Column(STUnicode(50))

    core = Column(STUnicode(9), index = True)
    isbn10 = Column(Unicode(10))
    isbn13 = Column(Unicode(13))
    valid = Column(Boolean)

    bookstore = Column(Unicode(16))
    bookstore_isbn_id = Column(Integer)

    def __init__(self, specific_isbn):
        self.raw = specific_isbn.raw
        #self.raw_simplified = utils.SimilarityCalculator.simplify(specific_isbn.raw)

        self.core = specific_isbn.core
        self.isbn10 = specific_isbn.isbn10
        self.isbn13 = specific_isbn.isbn13
        self.valid = specific_isbn.valid

        self.bookstore = specific_isbn.__tablename__[:-len("ISBN")]
        self.bookstore_isbn_id = specific_isbn.id

    to_normalize = []

    @staticmethod
    def normalize(session):
        for mini_isbn in MiniISBN.to_normalize:
            #print "To normalize: " + mini_isbn.raw

            master_ISBNs = MiniISBN.getMasterISBNCandidates(session, mini_isbn)

            equal_master_ISBNs = []

            for master_ISBN in master_ISBNs:
                if utils.SimilarityCalculator.eq_isbns(mini_isbn, master_ISBN):
                    equal_master_ISBNs.append(master_ISBN)

            master_ISBN = None

            if len(equal_master_ISBNs) == 0:
                #create masterISBN from miniISBN
                master_ISBN = final.MasterISBN(mini_isbn)
                master_ISBN.miniISBNs.append(mini_isbn)
            elif len(equal_master_ISBNs) == 1:
                #add miniISBN to masterISBN
                master_ISBN = equal_master_ISBNs[0]
                master_ISBN.miniISBNs.append(mini_isbn)
            elif len(equal_master_ISBNs) > 1:
                #master should be probably merged
                ratio = 0.0
                best_match = None
                for em in equal_master_ISBNs:
                    r = utils.SimilarityCalculator.isbns_ratio(mini_isbn, em)
                    if r > ratio:
                        best_match = em
                        ratio = r
                master_ISBN = best_match
                master_ISBN.miniISBNs.append(mini_isbn)

            session.add(master_ISBN)
            #session.commit()

        MiniISBN.to_normalize = []

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
