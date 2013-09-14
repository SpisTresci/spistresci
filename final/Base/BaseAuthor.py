from final.Final import FinalBase
from ..Comparable import *
from ..Mergeable import *
from Levenshtein import ratio
from final.FinalTypes import Name, LastName

class BaseAuthor(Comparable, FinalBase):
    id = Column(Integer, primary_key = True)

    name = Column(Unicode(255))
    firstName = Column(Name(32))
    middleName = Column(Name(32))
    lastName = Column(LastName(32))

    name_simplified = Column(Unicode(255), index = True)

    def cmp(self, other):
        if self.name == self.name:
            return merge(self, other, 1.0)
        else:
            r = self.Result()
            r.addRatio(cmp(self.lastName, other.lastName))
            r.addRatio(cmp(self.firstName, other.firstName))
            r.addRatio(cmp(self.middleName, other.middleName))

            return merge(self, other, max(r.result(), ratio(self.name, other.name) * 0.8))
