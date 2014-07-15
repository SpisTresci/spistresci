import final
import utils
from final.Base.BaseAuthor import *
from final.Base.BaseMini import *
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class MiniAuthor(BaseMini, BaseAuthor, Base):
    master_id = Column(Integer, ForeignKey('MasterAuthor.id'))
    #master by backref

    firstName_soundex = Column(Integer, index = True, default = 0)
    middleName_soundex = Column(Integer, index = True, default = 0)
    lastName_soundex = Column(Integer, index = True, default = 0)

    #lastName_simplified = Column(STUnicode(32))

    bookstore = Column(Unicode(16))
    bookstore_author_id = Column(Integer)

    def __init__(self, session, specificAuthor):
        self.session = session

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

        master_author = final.MasterAuthor(self)
        master_author.minis.append(self)
        self.session.add(master_author)

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
