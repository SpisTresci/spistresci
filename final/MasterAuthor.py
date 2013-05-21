import final
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()


class MasterAuthor(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    name = Column(STUnicode(255))
    firstName = Column(Unicode(32))
    middleName = Column(Unicode(32))
    lastName = Column(STUnicode(32))

    name_simplified = Column(STUnicode(255))
    #lastName_simplified = Column(STUnicode(32))

    #TODO: remove
    #firstName_soundex = Column(Integer, index = True, default = 0)
    #middleName_soundex = Column(Integer, index = True, default = 0)
    lastName_soundex = Column(Integer, index = True, default = 0)

    miniAuthors = relationship("MiniAuthor", backref = backref("masterAuthor", uselist = False))

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

