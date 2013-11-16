# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from spistresci.auth.views import authorization
from spistresci.constants import *
from spistresci.filters.filters import *
from constants import *

from ..search.views import STSearchQuerySet, STSearchView

class STBookView(STSearchView):
    template="book/index.html"

    def __call__(self, request, **kwargs):
        self.session = request.session
        request.GET = request.GET.copy()
        request.GET.update({"id":int(kwargs['book_id']), 'q':' '})
        return super(STBookView, self).__call__(request)

    def extra_context(self):
        extra = super(STBookView, self).extra_context()

        if self.results.get_args.keys() == ['id']:
            extra["hide_filters"] = True

        self.servicesInfo = self.getServicesInfo()

        extra['top_menu'] = getListOfTopMenuServices(self.request)
        extra['supported_formats'] = supported_formats
        extra["prefix"] = "s"

        self.load_values_if_exists_in_session(extra, ['isMenuHidden'])

        extra['filters'] = [
                                {
                                    'name':'SERWISY',
                                    'name_id':'services',
                                    'template_file':'filter/multiselect_list.html',
                                    'data':self.loadFilterState({'Wszystkie':[bookstore['name'] for bookstore in self.servicesInfo]}, "services")
                                },
                                {
                                    'name':'FORMATY',
                                    'name_id':'formats',
                                    'template_file':'filter/bullet_list.html',
                                    'data':self.loadFilterState(supported_formats, "formats")
                                },
                                {
                                    'name':'',
                                    'name_id':'services',
                                    'template_file': None,
                                    'data': self.loadFilterState({}, "services")
                                },
                                {
                                    'name':'SPOSÓB PŁATNOŚCI',
                                    'name_id':'formats',
                                    'template_file':'filter/bullet_list.html',
                                    'data':loadFilterState(None, {"Przez serwis":["DotPay", "ePrzelewy", "PayU", "Przelewy24.pl", "transferuj.pl", "YetiPay", "mPay", "SkyCash", "SMS", "PayPal", "karty płatnicze", "Przelewy24.pl"]}, "formats")
                                },
                                {
                                    'name':'CENA',
                                    'name_id':'price',
                                    'template_file':'filter/price.html',
                                    'data':self.loadFilterPriceState(['from', 'to'])
                                },
                            ]

        authorization(self.request, extra)

        return extra

    def get_results(self):
        r = super(STBookView, self).get_results()
        get = r.get_args
        print str(get)
        return r

    def parse_get_args(self):
        super(STBookView, self).parse_get_args()

        if "id" in self.request.GET:
            self.get_args["id"] = self.request.GET['id']

    def pre_filtering(self):
        condition = super(STBookView, self).pre_filtering()
        condition.next("and")
        condition.add({"id":self.get_args['id']})
        return condition





class STBookQuerySet(STSearchQuerySet):
    using = 'book_details'

    def __init__(self, using=None, query=None):
        super(STBookQuerySet, self).__init__(using='book_details')

    def convertResultsToProducts(self, results):
        results = super(STBookQuerySet, self).convertResultsToProducts(results)
        product = results[0]

        book =  {   'price': product.records[0]['price'],
                    'cover': product.records[0]['cover'],
                }

        for record in product.records:
            if record['price'] < book['price']:
                book['cover'] = record['cover']
                book['price'] = record['price']

        book['id'] = product.id
        book['authors'] = product.name
        book['title'] = product.title

        if product.description and len(product.description.split(" ")) > 75:
            book['description_short'] = " ".join(product.description.split(" ")[:75]) + "..."
        else:
            book['description_short'] = product.description if product.description else ""

        product.book = book

        return results

def book_redirect(request):
    return render(request, "book/redirect.html", request.GET)
