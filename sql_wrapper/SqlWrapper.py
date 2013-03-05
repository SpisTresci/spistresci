from sql_wrapper import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class SqlWrapper(object):
    Base = None
    engine = None

    @classmethod
    def init(cls):
        cls.getBaseClass().metadata.create_all(cls.getEngine())

    @classmethod
    def getBaseClass(cls):
        if cls.Base == None:
            cls.Base = declarative_base()
        return cls.Base

    @classmethod
    def getEngine(cls):
        if cls.engine == None:
            cls.engine = create_engine('mysql://root:Z0oBvgF1R3@localhost/st', echo=True)
        return cls.engine
