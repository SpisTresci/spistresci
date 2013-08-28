class DBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.object_name == 'eGazeciarzUser':
            return 'baza_calibre'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.object_name == 'eGazeciarzUser':
            return 'baza_calibre'
        else:
            return 'default'

    def allow_syncdb(self, db, model):
        if model._meta.object_name == 'eGazeciarzUser':
            return False
        return db == 'default'
