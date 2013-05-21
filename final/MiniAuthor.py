import final
import utils
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class MiniAuthor(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    master_id = Column(Integer, ForeignKey('MasterAuthor.id'))

    name = Column(STUnicode(255))
    firstName = Column(Unicode(32))
    middleName = Column(Unicode(32))
    lastName = Column(STUnicode(32))

    firstName_soundex = Column(Integer, index = True, default = 0)
    middleName_soundex = Column(Integer, index = True, default = 0)
    lastName_soundex = Column(Integer, index = True, default = 0)

    name_simplified = Column(STUnicode(255), index = True)
    #lastName_simplified = Column(STUnicode(32))

    bookstore = Column(Unicode(16))
    bookstore_author_id = Column(Integer)

    def __init__(self, specificAuthor):
        self.name = specificAuthor.name
        self.firstName = specificAuthor.firstName
        self.middleName = specificAuthor.middleName
        self.lastName = specificAuthor.lastName

        #TODO: remove
        #if specificAuthor.firstName and specificAuthor.firstName != "" and not utils.SimilarityCalculator.isInitial(specificAuthor.firstName):
        #    self.firstName_soundex = utils.soundexPL(utils.SimilarityCalculator.simplify(specificAuthor.firstName))

        #if specificAuthor.middleName and specificAuthor.middleName != "" and not utils.SimilarityCalculator.isInitial(specificAuthor.middleName):
        #    self.middleName_soundex = utils.soundexPL(utils.SimilarityCalculator.simplify(specificAuthor.middleName))

        if specificAuthor.lastName and specificAuthor.lastName != "":
            self.lastName_soundex = utils.soundexPL(utils.SimilarityCalculator.simplify(specificAuthor.lastName))

        self.name_simplified = utils.SimilarityCalculator.simplify(specificAuthor.name)
        #self.lastName_simplified = utils.SimilarityCalculator.simplify(specificAuthor.lastName)

        self.bookstore = specificAuthor.__tablename__[:-len("Author")]
        self.bookstore_author_id = specificAuthor.id

    to_normalize = []

    @staticmethod
    def normalize(session):
        for mini_author in MiniAuthor.to_normalize:
            #print "To normalize: " + mini_author.name

            master_authors = MiniAuthor.getMasterAuthorCandidates(session, mini_author)

            equal_master_authors = []

            for master_author in master_authors:
                if utils.SimilarityCalculator.eq_authors(mini_author, master_author):
                    equal_master_authors.append(master_author)

            master_author = None

            if len(equal_master_authors) == 0:
                #create masterAuthor from miniAuthor
                master_author = final.MasterAuthor(mini_author)
                master_author.miniAuthors.append(mini_author)
            elif len(equal_master_authors) == 1:
                #add miniAuthor to masterAuthor
                master_author = equal_master_authors[0]
                master_author.miniAuthors.append(mini_author)
            elif len(equal_master_authors) > 1:
                #master should be probably merged
                ratio = 0.0
                best_match = None
                for em in equal_master_authors:
                    r = utils.SimilarityCalculator.authors_ratio(mini_author, em)
                    if r > ratio:
                        best_match = em
                        ratio = r
                master_author = best_match
                master_author.miniAuthors.append(mini_author)

            session.add(master_author)
            #session.commit()

        MiniAuthor.to_normalize = []

    @staticmethod
    def normalize_find_candidates(mini_author):
        pass

    @staticmethod
    def getMasterAuthorCandidates(session, mini_author):
        r = []

        #master
        r.append(session.query(final.MasterAuthor).filter(final.MasterAuthor.name_simplified == utils.SimilarityCalculator.simplify(mini_author.name)).all())
        r.append(session.query(final.MasterAuthor).filter(final.MasterAuthor.lastName_soundex == utils.soundexPL(utils.SimilarityCalculator.simplify(mini_author.lastName))).all())

        #union on all lists in the list 'r'
        result = []
        for list_elem in r:
            result = list(set(result) | set(list_elem))

        return result
