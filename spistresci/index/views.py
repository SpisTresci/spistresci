# -*- coding: utf-8 -*-

from django.db.models import Count
from django.views.generic.base import TemplateView

from spistresci.blogger.models import BookRecommendation, BloggerProfile
from spistresci.models import (
    Bookstore,
    MasterBook,
    MiniBook,
    Promotion,
)


class HomePage(TemplateView):

    template_name = 'index.html'
    BOOK_LIMIT = 6
    RECOMENDATIONS_ON_FRONTPAGE = 4

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)

        context.update(self.getRandomReviews())

        context.update({
            'promominis': MiniBook.objects.filter(
                promotion__id=Promotion.PROMOTION_OF_THE_DAY
            ).order_by('?')[:self.BOOK_LIMIT],
            'bestsellers': {
                'mini_books': MiniBook.objects.filter(
                    bestseller_type=MiniBook.BESTSELLER__MANUALLY_SET
                ).all()[:self.BOOK_LIMIT],
                'master_books': MasterBook.objects.filter(
                    bestseller_type=MasterBook.BESTSELLER__MANUALLY_SET
                ).all()[:self.BOOK_LIMIT]
            },
            'new': {
                'mini_books': MiniBook.objects.filter(
                    new_type=MiniBook.NEW__MANUALLY_SET
                ).all()[:self.BOOK_LIMIT],
                'master_books': MasterBook.objects.filter(
                    new_type=MasterBook.NEW__MANUALLY_SET
                ).all()[:self.BOOK_LIMIT]
            },
            'bookstores_count': Bookstore.objects.count(),
            'minibooks_count': MiniBook.objects.count(),
        })

        return context

    def getRandomReviews(self):

        bloggers = BloggerProfile.objects.filter(
            user__recommendations__status=BookRecommendation.STATUS_PUBLICATED
        ).annotate(
            number_of_recs=Count('user__recommendations')
        ).filter(
            number_of_recs__gt=0
        ).order_by('?')[:self.RECOMENDATIONS_ON_FRONTPAGE]

        dic = {"blogger_reviews": []}

        for blogger in bloggers:
            dic["blogger_reviews"].append({
                "blogger": blogger,
                "recomendation": blogger.user.recommendations.order_by('?')[0]
            })

        return dic
