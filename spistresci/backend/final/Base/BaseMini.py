from ..Mergeable import *


class BaseMini(Mergeable):

    def merge_mini(self, other, result):
        if result >= self.accept_threshold:
            other.master.removeMini(other)
            self.master.addMini(other)
            return result, True
        return result, False

