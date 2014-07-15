from utils import logger_instance

class BaseFilter(object):
    def __init__(self, logger, params):
        self.params = params
        self.logger = logger

    def __str__(self):
        return self.__class__.__name__

    def __unicode__(self):
        return unicode(self.__class__.__name__)

    #each call of filter.run() should take a file 
    #and replace it with filtered one
    def run(self, file):
        pass


class DummyFilter(BaseFilter):
    def run(self, file):
        self.logger.info('Running %s on file %s' % (self, file))

