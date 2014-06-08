# -*- coding: utf-8 -*-

def getListOfTopMenuServices(request):
    list_of_services = [
        {'name':u'Spis Treści', 'url':'/'},
        {'name':u'eKundelek', 'url':'http://eKundelek.pl'},
     #   {'name':u'Ranking', 'url':'#'},
     #   {'name':u'Raporty', 'url':'#'},
    ]

    if request.user.is_authenticated() and request.user.username == 'admin':
        list_of_services.append({'name':u'Monitor', 'url':'/monitor/'})

    return list_of_services



supported_formats = {
    "ebook":["mobi", "epub", "pdf"],
    "audiobook":["mp3", "cd"],
    "druk":["ks"],
}

supported_formats_flat = [format for subgroup_format_list in supported_formats.values() for format in subgroup_format_list]
