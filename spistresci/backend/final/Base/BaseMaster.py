from ..Mergeable import *


class BaseMaster(Mergeable):
    def merge(self, other, result):
        if result >= self.accept_threshold:

            if type(self) != type(other):
                #Master & Mini
                other.master.removeMini(other)
                self.addMini(other)
            else:
                #Master & Master
                for mini in other.minis:
                    other.removeMini(mini)
                    self.addMini(mini)

            ret = result, True
            return ret

        ret = result, False
        return ret