# -*- coding: utf-8 -*-
from unidecode import unidecode
import re

def removePunctuation(word):
    punctuationList = [u'.', u',', u':', u';', u'!', u'?', u'...', u'…', u'-', u'(', u')', u'[', u']', u'{', u'}', u'<', u'>', u'⟨', u'⟩', u'"', u'„', u'”', u'«', u'»', u"'"]
    for p in punctuationList:
        word = word.replace(p, " ")
    return word

def simplify(s):
    return removeDiacritics(simplifyHyphens(s).lower()).strip()

def removeDiacritics(t):
    return unidecode(t)

def simplifyHyphens(string, error_msg = None):
    if string == None:
        return ""
    hyphenLike = [u'\u2010', u'\u2011', u'\u2012', u'\u2013', u'\u2014', u'\u2015']
    if any(char in string for char in hyphenLike):
        string = re.sub('[%s]' % ''.join(hyphenLike), "-", string)
    return string

def listToUnicode(_list, separator=', ',):
    if isinstance(_list, basestring):
        return unicode(_list)
    try:
        return separator.join([unicode(x) for x in  _list])
    except TypeError:
        if _list:
            return unicode(_list)
        else:
            return None
