from sqlwrapper import *

class GetOrCreateCache(object):
    cache = {}

    @classmethod
    def get_or_create(cls, session, id, dic):
        try:
            return cls.cache[id]
        except KeyError:
            cls.cache[id] = SqlWrapper.get_or_create_(session, cls, dic)
            session.add(cls.cache[id])
            return cls.cache[id]
