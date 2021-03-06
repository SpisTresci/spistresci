import re
import tempfile
import os
import shutil
from BaseFilters import BaseFilter


class RegexFilter(BaseFilter):
    def run(self, file):
        self.logger.info('Running %s on file %s' % (self, file))
        tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        flags = 0
        if bool(self.params.get('debug',False)):
            flags|= re.DEBUG
        if bool(self.params.get('ignorecase')):
            flags|= re.IGNORECASE
        if bool(self.params.get('locale',False)):
            flags|= re.LOCALE
        if bool(self.params.get('multiline',False)):
            flags|= re.MULTILINE
        if bool(self.params.get('dotall',False)):
            flags|= re.DOTALL
        if bool(self.params.get('unicode',False)):
            flags|= re.UNICODE
        if bool(self.params.get('verbose',False)):
            flags|= re.VERBOSE
        org = open(file, 'rU')
        #if you want to use , in pattern or replace list - escape it with \
        pattern_list = re.split(r'(?<!\\),', self.params.get('pattern_list',''))
        replace_list = re.split(r'(?<!\\),', self.params.get('replace_list',''))
        content = org.read()
        for (pattern, replace) in zip(pattern_list, replace_list):
            content = re.sub(str(pattern), str(replace), content, flags=flags)
        tmp.write(content)
        org.close()
        tmp.close()
        shutil.copy2(tmp.name, file)
        os.remove(tmp.name)

class Ads4Books(RegexFilter):
    def __init__(self, logger, params):
        params.setdefault('pattern_list',r'</.*?>\d+$')
        params.setdefault('replace_list',r'</products>')
        params.setdefault('ignorecase',True)
        RegexFilter.__init__(self, logger, params)
        
