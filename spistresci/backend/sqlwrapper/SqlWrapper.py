from sqlwrapper import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import event, DDL
from sqlalchemy.orm import joinedload
import urlparse

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

SQLITE_TRIGGER_INSERT = '''
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
    broadEngine = None
    defaults = {'scheme':'mysql', 'username':'root', 'password':'',
                'host':'localhost', 'database':'test', 'echo': 'False'}

    table_list = []

    @classmethod
    def init(cls, config_file = None, connectors = [], auto_write_to_db = True):
        config = utils.MultiLevelConfigParser(cls.defaults)
        if config_file:
            config.read(config_file)
        cls.scheme = config.get('DEFAULT', 'scheme')
        cls.username = config.get('DEFAULT', 'username')
        cls.password = config.get('DEFAULT', 'password')
        cls.host = config.get('DEFAULT', 'host')
        cls.database = config.get('DEFAULT', 'database')
        cls.echo = config.getboolean('DEFAULT', 'echo')
        cls.charset = config.get('DEFAULT', 'charset')
        cls.use_unicode = config.getint('DEFAULT', 'use_unicode')
        cls.create_db_if_not_exist = config.getboolean('DEFAULT', 'create_db_if_not_exist')
        cls.tables = [x for x in cls.getBaseClass().metadata.sorted_tables if any(con in x.name for con in connectors)]
        cls.table_list = [cls.getBaseClass().metadata.tables[x] for x in cls.table_list if cls.getBaseClass().metadata.tables.get(x) != None]
        cls.createTables(cls.table_list)
        if cls.tables and auto_write_to_db:
            cls.createTriggers()
            cls.createTables(cls.tables)

        #cls.getBaseClass().metadata.bind.execute("CREATE FUNCTION levenshtein RETURNS INT SONAME 'levenshtein.so'; CREATE FUNCTION levenshtein_k RETURNS INT SONAME 'levenshtein.so'; CREATE FUNCTION levenshtein_ratio RETURNS REAL SONAME 'levenshtein.so';")
        #print "ok"

    @classmethod
    def createTables(cls, tables=None):
        if not tables:
            tables = cls.tables
        cls.getBaseClass().metadata.bind = cls.getEngine()
        cls.getBaseClass().metadata.create_all(cls.getEngine(), tables=tables)


    @classmethod
    def createTriggers(cls):
        for t in cls.tables:
            tb = t.name
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
    def getNetLoc(cls):
        netloc = ''
        if cls.username:
            netloc += cls.username
            if cls.password:
                netloc += ':'
                netloc += cls.password
            netloc += '@'
        netloc += cls.host
        return netloc

    @classmethod
    def getEngine(cls):
        """
        This engine points to database which is specified in file[s] db[[.production/devel][.hostname]].ini
        """
        if cls.engine == None:
            netloc = cls.getNetLoc()
            urlparse.uses_netloc.append(cls.scheme)

            if cls.create_db_if_not_exist:
                cls.getBroadEngine().execute("CREATE DATABASE IF NOT EXISTS %s" % cls.database)

            query = ''
            if cls.charset:
                query='charset=%s' % cls.charset
            if cls.use_unicode:
                query+='&use_unicode=%d' % cls.use_unicode
            uri = urlparse.urlunparse((cls.scheme, netloc, cls.database, None, query, None))
            urlparse.uses_netloc.pop()
            cls.engine = create_engine(uri, echo = cls.echo, encoding = 'utf-8')

        return cls.engine

    @classmethod
    def getBroadEngine(cls):
        """
        This engine points to database by schema://user@hostname according to specified information from
        file[s] db[[.production/devel][.hostname]].ini, HOWEVER without specifying database, which allows
        create/drop various databases.
        """
        if cls.broadEngine == None:
            netloc = cls.getNetLoc()
            urlparse.uses_netloc.append(cls.scheme)
            uri = urlparse.urlunparse((cls.scheme, netloc, '', None, None, None))
            cls.broadEngine = create_engine(uri, echo = cls.echo, encoding = 'utf-8')

        return cls.broadEngine

    @classmethod
    def get_or_create_(cls, session, ClassName, d, param_name = None):
        c = None
        if param_name == None:
            c = session.query(ClassName).filter_by(**d).first()
        elif d.get(param_name) != None:
            c = session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()

        if not c:
            c = ClassName(**d)
        return c

    @classmethod
    def create_(cls, session, ClassName, d, param_name = None):
        c = ClassName(**d)
        return c


    @classmethod
    def get_(cls, session, ClassName, d, param_name=None):
        if param_name == None:
            return session.query(ClassName).filter_by(**d).first()
        else:
            return (session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()) if d.get(param_name) != None else None

    @staticmethod
    def isEgoistStrategyOn():
        return True
