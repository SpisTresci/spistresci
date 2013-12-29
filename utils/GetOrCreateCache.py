from sqlwrapper import *

class GetOrCreateCache(object):
    cache = {}

    @classmethod
    def get_or_create(cls, session, namespace, id, dic):
        try:
            return cls.cache[namespace][id]
        except KeyError:
            if cls.cache.get(namespace) == None:
                cls.cache[namespace]={}

            cls.cache[namespace][id] = SqlWrapper.get_or_create_(session, cls, dic)
            session.add(cls.cache[namespace][id])
            return cls.cache[namespace][id]
