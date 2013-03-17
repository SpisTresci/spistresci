from sql_wrapper import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event, DDL

import ConfigParser
import urlparse


class SqlWrapper(object):
    Base = None
    engine = None

    scheme = 'mysql'
    username = 'root'
    password = ''
    host = 'localhost'
    database = 'st'
    echo =  False

    @classmethod
    def init(cls, config_file=None, connectors=None):
        if config_file:
            config = ConfigParser.SafeConfigParser()
            config.read(config_file)
            cls.scheme = config.get('DEFAULT', 'scheme')
            cls.username = config.get('DEFAULT', 'username')
            cls.password = config.get('DEFAULT', 'password')
            cls.host = config.get('DEFAULT', 'host')
            cls.database = config.get('DEFAULT', 'database')
            cls.echo = config.getboolean('DEFAULT', 'echo')
        tables = [x for x in cls.getBaseClass().metadata.sorted_tables if any(con in x.name for con in connectors)]
        if tables:
            cls.createTriggers(tables, cls.scheme)
            cls.getBaseClass().metadata.create_all(cls.getEngine(), tables=tables)

    @classmethod
    def createTriggers(cls, tables, scheme):
        trigger_insert_command="""
            CREATE TRIGGER %sPriceOn%s AFTER %s ON %s
            FOR EACH ROW
            BEGIN
            INSERT INTO %sPrice(book_id, price, date) VALUES (NEW.id, NEW.price, NOW());
            END;
            """
        trigger_update_command="""
            CREATE TRIGGER %sPriceOn%s AFTER %s ON %s
            FOR EACH ROW
            BEGIN
            IF (NEW.price != OLD.price) THEN
            INSERT INTO %sPrice(book_id, price, date) VALUES (NEW.id, NEW.price, NOW());
            END IF;
            END;
            """
        for t in tables:
            tb=t.name
            if tb.endswith("Book"):
                event.listen(t, 'after_create', DDL(trigger_insert_command%(tb,"Insert","INSERT",tb,tb), on=scheme))
                event.listen(t, 'after_create', DDL(trigger_update_command%(tb,"Update","UPDATE",tb,tb), on=scheme))

    @classmethod
    def getBaseClass(cls):
        if cls.Base == None:
            cls.Base = declarative_base()
        return cls.Base

    @classmethod
    def getEngine(cls):
        if cls.engine == None:
            #cls.engine = create_engine('mysql://root:Z0oBvgF1R3@localhost/st', echo=True)
            netloc = ''
            if cls.username:
                netloc += cls.username
                if cls.password:
                    netloc += ':'
                    netloc += cls.password
                netloc += '@'
            netloc += cls.host    
            uri = urlparse.urlunparse((cls.scheme,netloc,cls.database,None,None,None))
            cls.engine = create_engine(uri, echo=cls.echo)
        return cls.engine
