# -*- coding: utf-8 -*-

list_of_services = [
    {'name':u'Spis Treści', 'url':'/'},
    {'name':u'eKundelek', 'url':'http://eKundelek.pl'},
    {'name':u'Ranking', 'url':'#'},
    {'name':u'Raporty', 'url':'#'},
]

supported_formats = {
    "ebook":["mobi", "epub", "pdf"],
    "audiobook":["mp3", "cd"],
}

supported_formats_flat = [format for subgroup_format_list in supported_formats.values() for format in subgroup_format_list]