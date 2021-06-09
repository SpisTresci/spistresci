from final.Final import FinalBase
from ..Comparable import *
from ..Mergeable import *
from Levenshtein import distance
import utils

class BaseISBN(Comparable, FinalBase):
    id = Column(Integer, primary_key = True)
    raw = Column(Unicode(50))
    core = Column(STUnicode(9))
    isbn10 = Column(Unicode(10))
    isbn13 = Column(Unicode(13))
    valid = Column(Boolean)

    def cmp(self, other):

        r = self.Result()

        if self.raw == other.raw and self.valid:
            r.addRatio(1.0)
        else:
            if self.isbn10 == other.isbn10 and self.valid:
                r.addRatio(1.0)
            elif self.isbn13 == other.isbn13 and self.valid:
                r.addRatio(1.0)
            elif self.core == other.core and self.valid:
                r.addRatio(0.95)
            elif self.raw == other.raw and not self.valid:
                r.addRatio(0.9)
            elif (not self.valid and other.valid) or (self.valid and not other.valid):
                i1_ = utils.Str.simplify(self.raw).replace("-", "")
                i2_ = utils.Str.simplify(other.raw).replace("-", "")

                if distance(i1_, i2_) == 1:
                    if i1_[:-1] == i2_[:-1]:  # checksum is different
                        r.addRatio(0.85)
                    else:
                        r.addRatio(0.75)
                elif distance(i1_, i2_) == 2:
                    r.addRatio(0.70)

        result = r.result()
        return merge(self, other, result)




