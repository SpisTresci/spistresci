import re
from pyisbn import *
import glob

class DataValidator(object):

    list_of_names = []
    supported_formats = ['cd', 'cd_mp3', 'dvd', 'epub', 'fb2', 'ks', 'mobi', 'mp3', 'pdf', 'txt', 'xml']
    
    #ks means - paperbook
    supported_persons = ['author', 'lector', 'redactor', 'translator']

    price_re = re.compile(r'^(\d*)([.,]?)(\d{0,2})$')

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validateFormats(dic, id, title)
        self.validateISBNs(dic, id, title)
        self.validatePrice(dic, id, title)
        self.validatePrice(dic, id, title, 'price_normal', -1)
        self.validateSize(dic, id, title)
        self.validateAuthors(dic, id, title)
        self.validateLectors(dic, id, title)
        self.validateTranslators(dic, id, title)
        self.validateLength(dic, id, title)


    def validateFormats(self, dic, id, title):
        format_list = []
        if dic.get("formats") != None:
            formats = dic["formats"]
            if isinstance(formats, basestring) and formats != "":
                if "," in formats:
                    format_list = filter(lambda x: x != "", formats.split(","))
                elif " " in formats:
                    format_list = formats.split(" ")
                else:
                    format_list = [formats]
            else:
                format_list = formats

        format_list = [x.strip().lower().replace('-','_') for x in format_list]

        if len(format_list) != len(set(format_list)):
            self.erratum_logger.warning("This same format declared more than once! connector: %s, id: %s, title: %s, formats: %s" % (self.name, id, title, formats))

        for x in format_list:
            if x not in self.supported_formats:
                self.erratum_logger.warning("Unsupported format! connector: %s, id: %s, title: %s, formats: %s" % (self.name, id, title, formats))

        dic['formats'] = format_list


    def validateISBNs(self, dic, id, title):
        original_isbn = dic.get('isbns')
        isbn_list = []
        if original_isbn != None and original_isbn != "":
            if not (isinstance(original_isbn, list) and not isinstance(original_isbn, basestring)):
                original_isbn = [original_isbn]

            for i in original_isbn:
                isbn_dic = {}
                try:
                    i = self.simplifyHyphens(i, "ISBN has wrong format! Some different unicode character was used instead of '-'. Connector: %s, original_isbn: %s, id: %s, title: %s" % (self.name, original_isbn, id, title))
                    i = i.lower().replace("-", "")
                    if "isbn" in i:
                        i = i.replace(i[i.find("isbn"):len("isbn")], "")

                    isbn_dic['raw'] = i
                    isbn = Isbn(i)
                    if isbn.validate() and (len(isbn.isbn) != 13 or (len(isbn.isbn) == 13 and isbn.isbn[0:3] in ['978', '979'])):
                        #without (len(isbn.isbn) != 13 or (len(isbn.isbn) == 13 and isbn.isbn[0:3] in ['978', '979'])) condition
                        #validate pass numbers which are EAN-13 but are not ISBN-13

                        isbn_dic['valid'] = True
                        if len(isbn.isbn) == 10:
                            isbn_dic['isbn10'] = isbn.isbn
                            isbn_dic['isbn13'] = isbn.convert()
                            isbn_dic['core'] = isbn.isbn[:-1]
                        elif len(isbn.isbn) == 13:
                            isbn_dic['isbn13'] = isbn.isbn
                            isbn_dic['isbn10'] = isbn.convert()
                            isbn_dic['core'] = isbn.convert()[:-1]
                        else:
                            isbn_dic['valid'] = False
                            self.erratum_logger.info("ISBN validation failed! connector: %s, original_isbn: %s, cannonical ISBN: %s, id: %s, title: %s" % (self.name, original_isbn, isbn.isbn, id, title))
                    else:
                        isbn_dic['valid'] = False
                        if len(i) == 10:
                            isbn_dic['core'] = isbn.isbn[:-1]
                        elif len(i) == 13:
                            isbn_dic['core'] = isbn.isbn[3:-1]
                        self.erratum_logger.info("ISBN validation failed! connector: %s, original_isbn: %s, cannonical ISBN: %s, id: %s, title: %s" % (self.name, original_isbn, isbn.isbn, id, title))

                except IsbnError:
                    if original_isbn == '':
                        self.erratum_logger.warning("Entry does not have ISBN! connector: %s, id: %s, title: %s" % (self.name, id, title))
                    else:
                        isbn_dic['valid'] = False
                        self.erratum_logger.info("ISBN has wrong format! connector: %s, original_isbn: %s, id: %s, title: %s" % (self.name, original_isbn, id, title))

                isbn_list.append(isbn_dic)

        dic['isbns'] = isbn_list

    def validatePrice(self, dic, id, title, price_tag_name = 'price', default_price=0):
        if type(default_price) is not int:
            raise TypeError('Default_price should be integer')
        
        original_price = dic.get(price_tag_name, default_price)
        if original_price != default_price and original_price != '':
            price_match = self.price_re.match(original_price)
            if not price_match:
                self.erratum_logger.warning("Entry has price in wrong format! connector: %s, id: %s, title: %s, price: %s" % (self.name, id, title, str(original_price)))
                dic[price_tag_name] = unicode(default_price)
            else:
                zl = int(('%1s'%price_match.groups()[0]).replace(' ','0'))*100
                gr = int(('%2s'%price_match.groups()[2]).replace(' ','0'))
                dic[price_tag_name] = unicode(zl+gr)
        else:
            dic[price_tag_name] = unicode(default_price)

    def validatePerson(self, person, id, title):
        pdict = {}
        person = person.strip()
        person = self.simplifyHyphens(person, "Authors has wrong format! Some different unicode character was used instead of '-'. Connector: %s, person: %s, id: %s, title: %s" % (self.name, person, id, title))
        person = person.replace(" - ", "-")

        while "  " in person:
            person = person.replace("  ", " ")

        # "J.T.Tomas" -> "J. T. Tomas"
        import regex
        p = ur'([\p{Lu}])\.([\p{Lu}])' #http://stackoverflow.com/q/4050381/
        s = r'\1. \2'
        u = regex.UNICODE
        person = regex.sub(p, s, regex.sub(p, s, person, u), u)

        if person != "":
            pdict["name"] = person

            names = [x.strip() for x in person.split(" ")]
            if len(names) == 2: #imie i nazwisko
                n1 = names[0].strip()
                n2 = names[1].strip()
                pdict["firstName"] = (n1 if self.isName(n1) else (n2 if self.isName(n2) else n1)).title()
                pdict["lastName"] = (n2 if self.isName(n1) else (n1 if self.isName(n2) else n2)).title()
                pdict["middleName"] = u""
            elif len(names) == 3:
                pdict["firstName"] = names[0].strip().title()
                pdict["middleName"] = names[1].strip().title()
                pdict["lastName"] = names[2].strip().title()
            else:
                pdict["firstName"] = pdict["middleName"] = pdict["lastName"] = u""

        return pdict


    def validateAuthors(self, dic, id, title):
        self.validatePersons(dic, id, title, 'authors')

    def validateLectors(self, dic, id, title):
        self.validatePersons(dic, id, title, 'lectors')

    def validateTranslators(self, dic, id, title):
        self.validatePersons(dic, id, title, 'translators')

    def validateRedactors(self, dic, id, title):
        self.validatePersons(dic, id, title, 'redactors')


    def validatePersons(self, dic, id, title, tag_name):
        if not any(tag_name[:-1] == role for role in self.supported_persons):
            raise DataValidatorError("tag_name <" + tag_name + "> is not supported!")

        if dic.get(tag_name) != None:
            if isinstance(dic.get(tag_name), basestring):
                dic[tag_name] = [unicode(x.strip()) for x in re.split("[,;]", dic[tag_name])]
            elif isinstance(dic.get(tag_name), list):
                dic[tag_name] = [unicode(x) for x in dic[tag_name]]

            persons = dic[tag_name]
            new_list_of_person_dicts = []
            if not (isinstance(persons, list) and not isinstance(persons, basestring)):
                persons = [persons]
            for person in persons:
                pdict = self.validatePerson(person, id, title)
                if pdict != {}:
                    new_list_of_person_dicts.append(pdict)

            if dic.get('persons') == None:
                dic['persons'] = []

            dic['persons'].append({unicode(tag_name):new_list_of_person_dicts})
            del dic[tag_name]

    def isName(self, word):
        return word in self.list_of_names

    def loadListOfNames(self):
        for file in glob.glob("data/names/*"):
            with open(file, 'rU') as f:
                for line in f:
                    self.list_of_names.append(line.strip())

    def validateSize(self, dic, id, title):
        pass

    def validateLength(self, dic, id, title):
        pass

    def simplifyHyphens(self, string, error_msg = None):
        if string == None:
            return ""

        hyphenLike = [u'\u2010', u'\u2011', u'\u2012', u'\u2013', u'\u2014', u'\u2015']
        if any(char in string for char in hyphenLike):
            if error_msg: self.erratum_logger.info(error_msg)
            string = re.sub('[%s]' % ''.join(hyphenLike), "-", string)
        return string

# exception classes
class DataValidatorError(Exception):
    """Base class for ConfigParser exceptions."""

    def _get_message(self):
        """Getter for 'message'; needed only to override deprecation in
        BaseException."""
        return self.__message

    def _set_message(self, value):
        """Setter for 'message'; needed only to override deprecation in
        BaseException."""
        self.__message = value

    # BaseException.message has been deprecated since Python 2.6.  To prevent
    # DeprecationWarning from popping up over this pre-existing attribute, use
    # a new property that takes lookup precedence.
    message = property(_get_message, _set_message)

    def __init__(self, msg = ''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__
