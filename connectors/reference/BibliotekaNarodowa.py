# -*- coding: utf-8 -*-
#!/usr/bin/env python
# from connectors.generic import *
# from sqlwrapper import *
# import re
#
# class BibliotekaNarodowa(XMLConnector, MARCConnector, ReferenceConnector):
#
#     #dict of xml_tag -> db_column_name translations
#     xml_tag_dict = {
#         "./titleInfo[not(@type)]/title":('title', ''),
#         #"./titleInfo[@type='alternative']/title":('title_alternative', ''),
#         #"./titleInfo[not(@type)]/subtitle":('subtitle', ''),
#         #"./titleInfo[@type='alternative']/subtitle":('subtitle_alternative', ''),
#         u"./name[@type='personal' and not(./role/roleTerm[@type='text' and .='Tł.']) and contains(./role/roleTerm[@type='text'],'creator')]/namePart[not(@type)]":('authors', ''),
#         u"./name[@type='personal' and ./role/roleTerm[@type='text' and .='creator'] and ./role/roleTerm[@type='text' and .='Tł.']]/namePart[not(@type)]":('translators', ''),
#         "./genre[@authority='marcgt']":('genre', ''),
#         "./originInfo/publisher":('publisher', ''),
#         "./originInfo/dateIssued[@encoding='marc']":('date', ''),
#         "./language/languageTerm":('lang', ''),
#         "./physicalDescription/form[@authority='marcform']":('form', ''),
#         "./identifier[@type='isbn']":('isbns', ''),
#         #"./identifier[@type='isbn']":('external_id', ''),
#     }
#
#     XML_FILE_SIZE_LIMIT = 5000
#     QUERY = 'isbn="9788300*"'
#
#     def fetchData(self):
#         self.save_time_of_("fetch_start")
#         self.conn = self.makeConnection()
#         self.fetchMods(self.QUERY)
#         self.save_time_of_("fetch_end")
#
#     def validate(self, dic):
#         id = dic.get('external_id')
#         title = dic.get('title')
#         self.validateLists(dic)
#         self.validateISBNs(dic, id, title)
#         self.validateAuthors(dic, id, title)
#         self.validateAuthors(dic, id, title, "translators")
#
#     def validateLists(self, dic):
#         for tag_name in dic.keys():
#             if dic.get(tag_name) != None:
#                 if isinstance (dic[tag_name], list) and len(dic[tag_name]) > 1:
#                     if isinstance(dic[tag_name][0], dict) or dic[tag_name][0] == None:
#                         dic[tag_name] = dic[tag_name][0]
#                     else:
#                         dic[tag_name] = unicode(dic[tag_name][0])
#
#     def validateAuthors(self, dic, id, title, tag_name='authors'):
#         if dic.get(tag_name) != None:
#             persons = dic[tag_name]
#             new_list_of_person_dicts=[]
#             pdict={}
#             if not (isinstance(persons, list) and not isinstance(persons, basestring)):
#                 persons = [persons]
#             for person in persons:
#                 pdict["name"] = person
#                 names = [x.strip() for x in person.split(",")]
#                 if len(names) == 2: #imie i nazwisko
#                     pdict["lastName"] = names[0].strip()
#                     firstNames = names[1]
#                     if " " in firstNames:
#                         first_and_middle = firstNames.split(" ")
#                         pdict["firstName"] = self.removeDotFromName(first_and_middle[0])
#                         pdict["middleName"] = self.removeDotFromName(first_and_middle[1])
#                     else:
#                         pdict["firstName"] = self.removeDotFromName(firstNames)
#                 elif len(names) == 1:
#                     print "1 - "  + person
#                 else:
#                     print str(len(names)) + " - "  + person
#
#                 new_list_of_person_dicts.append(pdict)
#
#             dic[tag_name] = new_list_of_person_dicts
#
#     def removeDotFromName(self, name):
#         return name[:-1] if (name.endswith(".") and self.isName(name[:-1])) else name
#
#
# Base = SqlWrapper.getBaseClass()
#
# class BibliotekaNarodowaBook(GenericBook, Base):
#     title = Column(Unicode(512), primary_key=True)                    #502
#     genre = Column(Unicode(16))                     #4
#     publisher = Column(Unicode(1024))               #118
#     date = Column(Unicode(4), primary_key=True)
#     lang = Column(Unicode(4))                       #
#     form = Column(Unicode(8))                       #
