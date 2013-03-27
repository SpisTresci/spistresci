from sql_wrapper import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event, DDL
import urlparse

import ConfigParser
import utils

MYSQL_TRIGGER_INSERT = '''
CREATE TRIGGER %(tb)sPriceOnInsert AFTER INSERT ON %(tb)s
FOR EACH ROW
BEGIN
INSERT INTO %(tb)sPrice(book_id, price, date) VALUES (NEW.id, NEW.price, NOW());
END;
'''
MYSQL_TRIGGER_UPDATE = '''
CREATE TRIGGER %(tb)sPriceOnUpdate AFTER UPDATE ON %(tb)s
FOR EACH ROW
BEGIN
IF (NEW.price != OLD.price) THEN
INSERT INTO %(tb)sPrice(book_id, price, date) VALUES (NEW.id, NEW.price, NOW());
END IF;
END;
'''

SQLITE_TRIGGER_INSERT= '''
CREATE TRIGGER %(tb)sPriceOnInsert AFTER INSERT ON %(tb)s
FOR EACH ROW
BEGIN
INSERT INTO %(tb)sPrice(book_id, price, date) VALUES (NEW.id, NEW.price, NOW());
END;
'''
SQLITE_TRIGGER_UPDATE = '''
CREATE TRIGGER %(tb)sPriceOnUpdate AFTER UPDATE ON %(tb)s
FOR EACH ROW
WHEN (NEW.price != OLD.price)
BEGIN
INSERT INTO %(tb)sPrice(book_id, price, date) VALUES (NEW.id, NEW.price, NOW());
END;
'''

TRIGGER_INSERT_DROP = 'DROP TRIGGER %(tb)sPriceOnInsert ;'

TRIGGER_UPDATE_DROP = 'DROP TRIGGER %(tb)sPriceOnUpdate ;'

class Triggers(utils.Enum):
    values_dict = {
    'TRIGGER_INSERT':{'mysql':MYSQL_TRIGGER_INSERT, 'sqlite':SQLITE_TRIGGER_INSERT},
    'TRIGGER_UPDATE':{'mysql':MYSQL_TRIGGER_UPDATE, 'sqlite':SQLITE_TRIGGER_UPDATE},
    'TRIGGER_INSERT_DROP':{'mysql':TRIGGER_INSERT_DROP, 'sqlite':TRIGGER_INSERT_DROP},
    'TRIGGER_UPDATE_DROP':{'mysql':TRIGGER_UPDATE_DROP, 'sqlite':TRIGGER_UPDATE_DROP}}
    values = values_dict.keys()

    @classmethod
    def get_trigger_ddl(cls, engine, trigger, table):
        return cls.values_dict[cls.to_str(trigger)][engine] % {'tb':table}

class SqlWrapper(object):
    Base = None
    engine = None
    defaults = {'scheme':'mysql', 'username':'root', 'password':'', 
                'host':'localhost', 'database':'test', 'echo': 'False'}




    @classmethod
    def init(cls, config_file=None, connectors=[], auto_write_to_db=True):
        config = ConfigParser.SafeConfigParser(cls.defaults)
        if config_file:
            config.read(config_file)
        cls.scheme = config.get('DEFAULT', 'scheme')
        cls.username = config.get('DEFAULT', 'username')
        cls.password = config.get('DEFAULT', 'password')
        cls.host = config.get('DEFAULT', 'host')
        cls.database = config.get('DEFAULT', 'database')
        cls.echo = config.getboolean('DEFAULT', 'echo')
        cls.tables = [x for x in cls.getBaseClass().metadata.sorted_tables if any(con in x.name for con in connectors)]
        if cls.tables and auto_write_to_db:
            cls.createTriggers()
            cls.createTables()

    @classmethod
    def createTables(cls):
        if cls.tables:
            cls.getBaseClass().metadata.bind = cls.getEngine()
            cls.getBaseClass().metadata.create_all(cls.getEngine(), tables=cls.tables)

    @classmethod
    def createTriggers(cls):
        for t in cls.tables:
            tb=t.name
            if tb.endswith("Book"):
                #triggers have to be implemented for scheme to use it
                event.listen(t, 'after_create',
                    DDL(Triggers.get_trigger_ddl(cls.scheme, Triggers.TRIGGER_INSERT, tb), on=cls.scheme))
                event.listen(t, 'after_create',
                    DDL(Triggers.get_trigger_ddl(cls.scheme, Triggers.TRIGGER_UPDATE, tb), on=cls.scheme))
                event.listen(t, 'before_drop',
                    DDL(Triggers.get_trigger_ddl(cls.scheme, Triggers.TRIGGER_INSERT_DROP, tb), on=cls.scheme))
                event.listen(t, 'before_drop',
                    DDL(Triggers.get_trigger_ddl(cls.scheme, Triggers.TRIGGER_UPDATE_DROP, tb), on=cls.scheme))

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
            urlparse.uses_netloc.append(cls.scheme)
            uri = urlparse.urlunparse((cls.scheme,netloc,cls.database,None,None,None))
            urlparse.uses_netloc.pop()
            cls.engine = create_engine(uri, echo = cls.echo)
        return cls.engine
