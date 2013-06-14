import os
from connectors.generic import *
import lxml.html as et
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class ebooks43(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./div[@class='book_box_title']/a":('title', ''),
        "./a[@href]":('url', ''),
        "./a/img[@src]":('cover', ''),
        "./div[@class='book_box_autor']":('authors', ''),
        "./div[@class='book_box_format']":('formats', ''),
        "./div[@class='book_box_desc']":('description', ''),
    }

    def weHaveToGoDeeper(self, root, depth):
        return root.xpath("//div[@class='book_box_content']")

    def get_et(self):
        return et

    def adjust_parse(self, dic):
        if dic.get('formats'):
            dic['formats'] = dic['formats'].replace("Format: ", "")
        if dic.get('url'):
            dic['url'] = "http://www.ebooks43.pl" + dic['url']
            dic['external_id'] = dic['url'].split(",")[-2]
        if dic.get('cover'):
            dic['cover'] = "http://www.ebooks43.pl" + dic['cover']
        if dic.get('description'):
            dic['description'] = dic['description'].strip()

class ebooks43Book(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128))            #70
    url = Column(Unicode(128))              #108
    #price
    #price_normal
    #authors
    cover = Column(Unicode(64))             #50
