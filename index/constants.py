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

blogger_reviews=[
    {
        "blogger":{
            "firstName":u"Agnieszka",
            "lastName":u"Tatera",
            "gender":"female",
            "signature":u"agnieszka_tatera_signature.png",
        },
        "url":"http://ksiazkowo.wordpress.com/adres-strony-z-recenzja",
        "cover":"http://www.publio.pl/files/product/card/5d/5e/b4/85779-papierowy-ksiezyc-andrea-camilleri-1.jpg",
        "title":u"Excepteur sint occaecat cupidatat",
        "content":u"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "rating":u"Zdecydowanie polecam!",
        "blogUrl":"http://ksiazkowo.wordpress.com",
        "blogName":u"Książkowo",
    },
    #{
    #    "blogger":{
    #        "firstName":u"Andrzej",
    #        "lastName":u"Tucholski",
    #        "gender":"male",
    #        "signature":u"andrzej_tucholski_signature.png",
    #    },
    #    "url":"http://jestKultura.pl/adres-strony-z-recenzja",
    #    "cover":"http://ecsmedia.pl/c/kakrachan-tom-1-sagi-atlanci-p-iext22994551.jpg",
    #    "title":u"Ut enim ad minim veniam",
    #    "content":u"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    #    "rating":u"Jedna z lepych w serii.",
    #    "blogUrl":"http://jestKultura.pl",
    #    "blogName":u"jestKultura.pl",
    #},
    {
        "blogger":{
            "firstName":u"Anna",
            "lastName":u"Matusewicz",
            "gender":"female",
            "signature":u"anna_matusewicz_signature.png",
        },
        "url":"http://misja-ksiazka.pl/adres-strony-z-recenzja",
        "cover":"http://www.koobe.pl/static/33/33492/img/c528fb9a70b5241934b128b26438daff_226_0_n_100/978-83-7480-299-4.jpg",
        "title":u"Laboris nisi ut aliquip",
        "content":u"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "rating":u"Przeciętna jak na tego autora.",
        "blogUrl":"http://misja-ksiazka.pl",
        "blogName":u"misja-ksiazka.pl",
    },
    {
        "blogger":{
            "firstName":u"Iza",
            "lastName":u"Raducka",
            "gender":"female",
            "signature":u"iza_raducka_signature.png",
        },
        "url":"http://czytadelko.blox.pl/adres-strony-z-recenzja",
        "cover":"http://www.publio.pl/files/product/card/32/25/74/66371-wycieczka-do-tindari-andrea-camilleri-1.jpg",
        "title":u"Laboris nisi ut aliquip",
        "content":u"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "rating":u"Czytałam ją trzeci raz, więc nie jestem obiektywna ;)",
        "blogUrl":"http://czytadelko.blox.pl",
        "blogName":u"czytadelko.blox.pl",
    },
    {
        "blogger":{
            "firstName":u"Maja",
            "lastName":u"Sieńkowska",
            "gender":"female",
            "signature":u"maja_sieńkowska_signature.png",
        },
        "url":"http://wieczniezaczytana.pl/adres-strony-z-recenzja",
        "cover":"http://woblink.com/storable/pub_photos/190747-wiele-demonow.jpg",
        "title":u"Consectetur adipisicing elit",
        "content":u"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "rating":u"Warto czytać do końca ;)",
        "blogUrl":"http://wieczniezaczytana.pl",
        "blogName":u"WiecznieZaczytana.pl",
    },
    {
        "blogger":{
            "firstName":u"Dariusz",
            "lastName":u"Dłużeń",
            "gender":"male",
            "signature":u"dariusz_dłużeń_signature.png",
        },
        "url":"http://alekulturka.com/adres-strony-z-recenzja",
        "cover":"http://1.bp.blogspot.com/-tPBP-LcjCvI/Ufkh6O2POgI/AAAAAAAAb10/rlvjoh6-9-w/s400/stephen-king-joyland-cover-okladka+(1).jpg",
        "title":u"Consectetur adipisicing elit",
        "content":u"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "rating":u"4/6",
        "blogUrl":"http://alekulturka.com",
        "blogName":u"AleKulturka.com",
    },
]
