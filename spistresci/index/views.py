# -*- coding: utf-8 -*-
from django.shortcuts import render
from spistresci.auth.views import authorization
from spistresci.constants import *
from spistresci.blogger.models import BookRecommendation, BloggerProfile
from spistresci.models import MiniBook, Bookstore, Promotion

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


    minis = MiniBook.objects.filter(id__in = range(10))

    promo_day = Promotion.objects.get(id=Promotion.PROMOTION_OF_THE_DAY)

    for mini in minis:
        promo_day.mini_books.add(mini)

    promominis = MiniBook.objects.filter(
        promotion__id=Promotion.PROMOTION_OF_THE_DAY
    ).order_by('?')[:6]

    c['promominis'] = promominis


    return render(request, 'index.html', c)
