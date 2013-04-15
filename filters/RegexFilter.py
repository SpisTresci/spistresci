import re
import tempfile
import os
import shutil
from BaseFilters import BaseFilter
try:
  from collections import OrderedDict
except ImportError:
  from utils.compatibility import OrderedDict


class RegexFilter(BaseFilter):
    def run(self, file):
        self.logger.info('Running %s on file %s' % (self, file))
        print 'PARAMS:',self.params
        tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        flags = 0
        if bool(self.params.get('debug',False)):
            print 'PZ re.DEBUG'
            flags|= re.DEBUG
        if bool(self.params.get('ignorecase')):
            flags|= re.IGNORECASE
            print 'PZ re.IGNORECASE'
        if bool(self.params.get('locale',False)):
            flags|= re.LOCALE
            print 'PZ re.LOCALE'
        if bool(self.params.get('multiline',False)):
            flags|= re.MULTILINE
            print 'PZ re.MULTILINE'
        if bool(self.params.get('dotall',False)):
            flags|= re.DOTALL
            print 'PZ re.DOTALL'
        if bool(self.params.get('unicode',False)):
            flags|= re.UNICODE
            print 'PZ re.UNICODE'
        if bool(self.params.get('verbose',False)):
            flags|= re.VERBOSE
            print 'PZ re.VERBOSE'
        org = open(file, 'rU')
        #if you want to use , in pattern or replace list - escape it with \
        pattern_list = re.split(r'(?<!\\),', self.params.get('pattern_list',''))
        replace_list = re.split(r'(?<!\\),', self.params.get('replace_list',''))
        content = org.read()
        for (pattern, replace) in zip(pattern_list, replace_list):
            content = re.sub(pattern, replace, content, flags=flags)
        tmp.write(content)
        org.close()
        tmp.close()
        print tmp.name
        shutil.copy2(tmp.name, file)
        os.remove(tmp.name)
