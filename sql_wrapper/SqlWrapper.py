from sql_wrapper import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event, DDL



class SqlWrapper(object):
    Base = None
    engine = None

    @classmethod
    def init(cls):
        cls.createTriggers();
        cls.getBaseClass().metadata.create_all(cls.getEngine())

    @classmethod
    def createTriggers(cls):
        trigger_command="""
            CREATE TRIGGER %sPriceOn%s AFTER %s ON %s
            FOR EACH ROW
            BEGIN
            INSERT INTO %sPrice(book_id, price, date) VALUES (NEW.id, NEW.price, NOW());
            END;
            """
        for t in cls.getBaseClass().metadata.sorted_tables:
            tb=t.name
            if tb.endswith("Book"):
                for c in ["Insert", "Update"]:
                    event.listen(t, 'after_create', DDL(trigger_command%(tb,c,c,tb,tb), on="mysql"))

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
