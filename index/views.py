# -*- coding: utf-8 -*-
from django.shortcuts import render
from spistresci.auth.views import authorization
from spistresci.constants import *
from constants import *

group_of_books=[
    {
        "name":u"BESTSELLERY",
        "list":[
            {
                "title":u"Pułapka na martwego",
                "cover":"http://www.koobe.pl/static/33/33492/img/c528fb9a70b5241934b128b26438daff_226_0_n_100/978-83-7480-299-4.jpg?1368001334",
                "author":u"Charlaine Harris",
                "formats":["epub", "mobi"],
                "price":"23.97",
            },
            {
                "title":u"Wiele demonów",
                "cover":"http://woblink.com/storable/pub_photos/190747-wiele-demonow.jpg",
                "author":u"Jerzy Pilch",
                "formats":["epub", "mobi"],
                "price":"24.90",
            },
            {
                "title":u"Chustka",
                "cover":"http://woblink.com/storable/pub_photos/189960-chustka.jpg",
                "author":u"Joanna Sałyga",
                "formats":["epub", "mobi"],
                "price":"13.74",
            },
        ]
    },
    {
        "name":u"PROMOCJE",
        "list":[
            {
                "title":u"Droga 66",
                "cover":"http://static.virtualo.pl/media_images/normal/123056.jpg",
                "author":u"Dorota Warakomska",
                "formats":["epub", "mobi"],
                "price":"19.95",
            },
            {
                "title":u"Wycieczka do Tindari",
                "cover":"http://www.publio.pl/files/product/card/32/25/74/66371-wycieczka-do-tindari-andrea-camilleri-1.jpg",
                "author":u"Andrea Camilleri",
                "formats":["epub", "mobi"],
                "price":"10.80",
            },
            {
                "title":u"Papierowy księżyc",
                "cover":"http://www.publio.pl/files/product/card/5d/5e/b4/85779-papierowy-ksiezyc-andrea-camilleri-1.jpg",
                "author":u"Andrea Camilleri",
                "formats":["epub", "mobi"],
                "price":"10.80",
            },
        ]
    },
    {
        "name":u"NOWOŚCI",
        "list":[
            {
                "title":u"Ruiny",
                "cover":"http://woblink.com/storable/pub_photos/229765-ruiny.jpg",
                "author":u"Orson Scott Card",
                "formats":["epub", "mobi"],
                "price":"16.80",
            },
            {
                "title":u"Kakrachan Tom I sagi Atlanci",
                "cover":"http://ecsmedia.pl/c/kakrachan-tom-1-sagi-atlanci-p-iext22994551.jpg",
                "author":u"Olis Nari Lang",
                "formats":["epub", "mobi"],
                "price":"19.00",
            },
            {
                "title":u"Zwycięzca bierze wszystko",
                "cover":"http://www.koobe.pl/static/33/33799/img/e9ded486d10de4b3fbb92c3e1d39c9e1_226_0_n_100/jadowska03zwyciezcabierzewszystkocover.jpg?1375098758",
                "author":u"Aneta Jadowska",
                "formats":["epub", "mobi", "pdf"],
                "price":"28.76",
            },
        ]
    },
]

def index(request):
    c = {'top_menu':getListOfTopMenuServices(request)}
    c.update({'path':request.path})
    authorization(request, c)
    c['request'] = request

    import random

    for group in group_of_books:
        random.shuffle(group['list'])

    c['group_of_books']=group_of_books

    random.shuffle(blogger_reviews)
    c['blogger_reviews']=blogger_reviews[:3]
    return render(request, 'index.html', c)
