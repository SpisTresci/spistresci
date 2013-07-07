# -*- coding: utf-8 -*-
# from django.template.loader import POST_template
#from django.template import Context
#from django.http import HttpResponse

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
#import os
from django.shortcuts import render_to_response
from haystack.query import SearchQuerySet
from haystack.views import SearchView

def index(request):
    return render_to_response('index.html')

class STSearchView(SearchView):

    template='search.html'

    def extra_context(self):
        extra = super(STSearchView, self).extra_context()

        servise_names = ["abooki.pl", "albertus.pl", "audeo.pl", "audiobook.pl", "audioteka.pl", "barbelo.com.pl", "bezkartek.pl", "bezokladki.pl", "booki25.pl", "bookio.pl", "bookmaster.pl", "bookoteka.pl", "bookson.pl", "cdp.pl", "czarty.pl", "sklep.czatroom.pl", "czytajtanio.pl", "czeskieklimaty.pl", "czytam.pl", "dobryebook.pl", "ekiosk.pl", "eporadniki.pl", "etekst.pl", "ebooki24.pl", "ebook.memento.pl", "ebook.pl", "ebooki123.pl", "ebooki.allegro.pl", "ebooki.orange.pl", "ebooki.tmobile.pl", "ebookomania.pl", "eBookpoint.pl", "helion.pl", "onepress.pl", "sensus.pl", "septem.pl", "ebookowo.pl", "ebookowo.pl", "ebooks43.pl", "eclicto.pl", "empik.pl", "escapemagazine.pl", "fabryka.pl", "ksiazki.pl", "kodeksywmp3.pl", "fantastykapolska.pl", "gandalf.com.pl", "gutenberg.org", "iBook.net.pl" ]
        services = zip(range(len(servise_names)), servise_names)
        extra["services"] = services
        extra["prefix"] = "s"

        return extra

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
