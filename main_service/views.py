# -*- coding: utf-8 -*-
# from django.template.loader import POST_template
#from django.template import Context
#from django.http import HttpResponse

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
#import os
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from haystack.query import SearchQuerySet, SQ
from haystack.views import SearchView

def index(request):
    return render_to_response('index.html')

class STSearchView(SearchView):

    template='search.html'

    def __call__(self, request):
        self.session = request.session
        return super(STSearchView, self).__call__(request)

    def get_results(self):
        condition = None
        for key, value in self.session.items():
            if key.startswith("filter_format_") and value:
                if not condition:
                    condition = SQ(**{key.replace("filter_", ""):value})
                else:
                    condition &= SQ(**{key.replace("filter_", ""):value})

        results = self.form.search().filter(condition) if condition else self.form.search()

        for key, value in self.session.items():
            if key.startswith("filter_format_") and value:

                format=key.replace("filter_", "")
                for result in results:
                    result['records'] = [record for record in result['records'] if record[format]]

        return results

    def extra_context(self):
        extra = super(STSearchView, self).extra_context()

        servise_names = ["abooki.pl", "albertus.pl", "audeo.pl", "audiobook.pl", "audioteka.pl", "barbelo.com.pl", "bezkartek.pl", "bezokladki.pl", "booki25.pl", "bookio.pl", "bookmaster.pl", "bookoteka.pl", "bookson.pl", "cdp.pl", "czarty.pl", "sklep.czatroom.pl", "czytajtanio.pl", "czeskieklimaty.pl", "czytam.pl", "dobryebook.pl", "ekiosk.pl", "eporadniki.pl", "etekst.pl", "ebooki24.pl", "ebook.memento.pl", "ebook.pl", "ebooki123.pl", "ebooki.allegro.pl", "ebooki.orange.pl", "ebooki.tmobile.pl", "ebookomania.pl", "eBookpoint.pl", "helion.pl", "onepress.pl", "sensus.pl", "septem.pl", "ebookowo.pl", "ebookowo.pl", "ebooks43.pl", "eclicto.pl", "empik.pl", "escapemagazine.pl", "fabryka.pl", "ksiazki.pl", "kodeksywmp3.pl", "fantastykapolska.pl", "gandalf.com.pl", "gutenberg.org", "iBook.net.pl" ]
        services = zip(range(len(servise_names)), servise_names)
        extra["services"] = services
        extra["prefix"] = "s"

        if 'isMenuHidden' in self.request.session:
            extra["isMenuHidden"] = self.request.session['isMenuHidden']


        extra['filters'] = [
        {'name':'FORMATY',
         'subgroups':[
            {'name':'eBooki', 'items':self.load_formats_from_session([u'epub', u'mobi', u'pdf'])},
            {'name':'AudioBooki', 'items':self.load_formats_from_session([u'mp3', u'cd-audio', u'cd-mp3'])},
         ]
        }
       ]

        return extra

    def load_formats_from_session(self, format_list):
        r=[]
        for format in format_list:
            if 'filter_format_'+format in self.session:
                r.append({'name':format, 'value':self.session['filter_format_'+format]})
            else:
                r.append({'name':format, 'value':False})
        return r

class STSearchQuerySet(SearchQuerySet):

    def post_process_results(self, results):

        to_cache = []

        for result in results:

            formats = [attr.replace("format_", "").upper() for attr, value  in result.__dict__.iteritems() if str(attr).startswith("format_") and value]
            result.formats = formats
            result._additional_fields.append("formats")

            price_lowest = int(result.price[0])
            price_corrected = []
            for price in result.price:
                if int(price) < price_lowest:
                    price_lowest = int(price)
                price_corrected.append(str("%.2f" % (int(price)/100.0)))

            result.price = price_corrected
            price_lowest = str("%.2f" % (price_lowest/100.0))

            result.price_lowest = price_lowest
            result._additional_fields.append("price_lowest")

            records = []
            for price, bookstore, url, cover, format_mobi, format_pdf, format_epub, format_cd, format_mp3 in zip (result.price, result.bookstore, result.url, result.cover, result.mini_format_mobi, result.mini_format_pdf, result.mini_format_epub, result.mini_format_cd, result.mini_format_mp3):
                record={}
                for var_name in ["price", "bookstore", "url", "cover", "format_mobi", "format_pdf", "format_epub", "format_cd", "format_mp3"]:
                    record[var_name] = eval(var_name)

                record["formats"] = [attr.replace("format_", "").upper() for attr, value  in record.iteritems() if str(attr).startswith("format_") and value]

                records.append(record)

            result.records = records
            result._additional_fields.append("records")

            if len(records) > 0:
                result.cover = records[0]["cover"]
            else:
                result.cover = ""

            result._additional_fields.append("cover")

            to_cache.append(dict((i, getattr(result, i, None)) for i in result._additional_fields))

        return to_cache


def hide_menu(request, value):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    request.session['isMenuHidden'] = bool(int(value))

    return HttpResponse('ok')

def set_filter(request, type, key, value):

    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    if type == 'format':
        request.session['filter_format_' + key.strip()] = bool(value)
        return HttpResponse('ok')

def clear_filter(request, type):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    if type == 'format':
        for key in request.session.keys():
            if key.startswith('filter_format_'):
                del request.session[key]

    return HttpResponse('ok')
