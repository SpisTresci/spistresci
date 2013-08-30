from Ceneo import Ceneo
import re


class FormatInTitleConnector(Ceneo):

    def __init__(self, name = None, limit_books = 0):
        super(FormatInTitleConnector, self).__init__(name, limit_books)
        self.supported_formats = sorted(self.supported_formats, cmp = lambda x, y: cmp(len(x), len(y)), reverse = True)
        self.accepted_suffix_patterns = self.config.get('accepted_suffix_patterns', '')
        self.format_in_title_split_regex = self.config.get('format_in_title_split_regex', '!|\?|,|\.|')


    '''Note: This is dirty hack, but this is because Abooki xml is broken'''
    def _clear_suffixes_from_config(self, suffix):
        if self.accepted_suffix_patterns:
            for x in self.accepted_suffix_patterns.split(','):
                suffix = re.sub(x, '', suffix)
        return suffix

    def validateFormats(self, dic, id, title):
        format_string = dic.get('formats')
        if format_string:
            format_string = format_string.lower()
        org_format_string = format_string
        format_list = []
        for sf in self.supported_formats:
            if sf in format_string:
                format_list.append(sf)
                format_string = format_string.replace(sf, '')
            if not format_string:
                break
        cleared_format_string = ''
        dic['formats'] = format_list
        if format_string:
            format_string = self._clear_suffixes_from_config(format_string)
        if format_string:
            self.erratum_logger.warning("Unsupported format! connector: %s, id: %s, title: %s, format: %s" % (self.name, id, title, org_format_string))
            self.erratum_logger.debug("Unsupported format!. connector %s, id: %s, tile %s, format string left is: %s" % (self.name, id, title, format_string))

    def adjust_parse(self, dic):
        title = dic['title']
        split_regex = self.format_in_title_split_regex
        splited = re.split(split_regex,  dic['title'])
        if len(splited) > 1:
            format_string = splited[-1].strip()
            lowered_format = format_string.lower()
            if any(sf in lowered_format for sf in self.supported_formats):
                #if formats found in XML do not set it here
                if not dic.get('formats'):
                    dic['formats'] = unicode(lowered_format)

                #only replece info in title
                title = title.replace(format_string, '')
                split_regex = ' *(%s) *$' % split_regex
                dic['title'] = re.sub(split_regex, '', title)
                return
        dic.setdefault('formats', '')
