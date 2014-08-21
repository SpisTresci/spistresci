# -*- coding: utf-8 -*-
from django.shortcuts import render
from spistresci.auth.views import authorization
from spistresci.constants import *
from spistresci.blogger.models import BookRecommendation, BloggerProfile
from spistresci.models import MiniBook, Bookstore

group_of_books=[{"name": u"BESTSELLERY"}, {"name": u"NOWOŚCI"},{"name":u"PROMOCJE"}]
RECOMENDATIONS_ON_FRONTPAGE = 4

def getRandomReviews():

    from django.db.models import Count
    bloggers = BloggerProfile.objects.filter(user__recommendations__status=BookRecommendation.STATUS_PUBLICATED).annotate(number_of_recs=Count('user__recommendations')).filter(number_of_recs__gt=0).order_by('?')[:RECOMENDATIONS_ON_FRONTPAGE]

    dic = {"blogger_reviews":[]}

    for blogger in bloggers:
        dic["blogger_reviews"].append({"blogger": blogger, "recomendation": blogger.user.recommendations.order_by('?')[0]})

    return dic


def index(request):
    c = {'top_menu':getListOfTopMenuServices(request)}
    c.update({'path':request.path})
    authorization(request, c)
    c['request'] = request

    c['group_of_books']=group_of_books

    c.update(getRandomReviews())
    c['minibooks'] = MiniBook.objects.count()
    c['bookstores'] = Bookstore.objects.count()

    return render(request, 'index.html', c)
