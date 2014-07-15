import final
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()
from final.Base.BaseAuthor import *
from final.Base.BaseMaster import *

class MasterAuthor(BaseMaster, BaseAuthor, Base):
    #lastName_simplified = Column(STUnicode(32))

    #TODO: remove
    #firstName_soundex = Column(Integer, index = True, default = 0)
    #middleName_soundex = Column(Integer, index = True, default = 0)
    lastName_soundex = Column(Integer, index = True, default = 0)

    minis = relationship("MiniAuthor", backref = backref("master", uselist = False))

    def __init__(self, mini_author):
        if not isinstance(mini_author, final.MiniAuthor):
            raise Exception("MasterAuthor can be initialized only by MiniAuthor")

        self.name = mini_author.name
        self.firstName = mini_author.firstName
        self.middleName = mini_author.middleName
        self.lastName = mini_author.lastName

        self.name_simplified = mini_author.name_simplified
        #self.lastName_simplified = mini_author.lastName_simplified

        #self.firstName_soundex = mini_author.firstName_soundex
        #self.middleName_soundex = mini_author.middleName_soundex
        self.lastName_soundex = mini_author.lastName_soundex

    def mergeWith(self, masterauthors):
        #todo REMOVE
        pass

    #########################

    def addMini(self, other):
        pass

    def removeMini(self, other):
        pass
