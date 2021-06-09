from sqlwrapper import *
import final
Base = SqlWrapper.getBaseClass()

class BaseCompare(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    id = Column(Integer, primary_key=True)

    def __init__(self, item_low, item_high, result, merged):
        self.item_low = item_low
        self.item_high = item_high
        self.result = result
        self.merged = merged


    cache = None

    @classmethod
    def get(cls, item_low, item_high, session = None):
        if not session:
            session = final.Final.session
        if not cls.cache:
            all=session.query(cls).all()
            cls.cache = {}
            for item in all:
                id = (item.item_low_id, item.item_high_id) if item.item_low_id < item.item_high_id else (item.item_high_id, item.item_low_id)
                cls.cache[id] = item

        id = (item_low.id, item_high.id) if item_low.id < item_high.id else (item_high.id, item_low.id)
        return cls.cache.get(id, None)

    @classmethod
    def set(cls, item_low, item_high, (result, merged), session = None):
        if not session:
            session = final.Final.session
        cached = cls(item_low, item_high, result, merged)
        session.add(cached)

        cls.cache[(item_low.id, item_high.id) if item_low.id < item_high.id else (item_high.id, item_low.id)] = cached
        return result, merged



    #item_low_id = Column(Integer, ForeignKey('MiniAuthor.id'))
    @declared_attr
    def item_low_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__[:-len("Compare")]+'.id'), index=True)

    #item_low = relationship("MiniAuthor", uselist=False, foreign_keys=[item_low_id])
    @declared_attr
    def item_low(cls):
        return relationship(cls.__tablename__[:-len("Compare")], uselist=False, primaryjoin="%s.item_low_id==%s.id" % (cls.__tablename__,cls.__tablename__[:-len("Compare")]) )


    #item_high_id = Column(Integer, ForeignKey('MiniAuthor.id'))
    @declared_attr
    def item_high_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__[:-len("Compare")]+'.id'), index=True)

    #item_high = relationship("MiniAuthor", uselist=False, foreign_keys=[item_high_id])
    @declared_attr
    def item_high(cls):
        return relationship(cls.__tablename__[:-len("Compare")], uselist=False, primaryjoin="%s.item_high_id==%s.id" % (cls.__tablename__,cls.__tablename__[:-len("Compare")]))

    result = Column(Float)
    ignore = Column(Boolean, default=False)
    merged = Column(Boolean, default=False)

    @declared_attr
    def algorithm_id(cls):
        return Column(Integer, ForeignKey('MergeAlgorithm.id'))

    @declared_attr
    def algorithm(cls):
        return relationship("MergeAlgorithm", uselist=False)


