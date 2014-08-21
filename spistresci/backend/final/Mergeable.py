
def merge(obj1, obj2, result):
    if not (isinstance(obj1, Mergeable) and isinstance(obj1, Mergeable)):
        raise Exception("Given object is not an instance of Margeable class.")

    #return 0.0, False
    return obj1.merge(obj2, result)

class Mergeable(object):
    def merge(self, other, result):
        raise NotImplementedError
