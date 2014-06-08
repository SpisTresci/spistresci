# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseNotAllowed
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet, SQ
from haystack.views import SearchView
from haystack.forms import *
from spistresci.auth.views import authorization
from spistresci.constants import *
import random

class STSearchForm(ModelSearchForm):
    formats = forms.CharField(required=False, widget=forms.HiddenInput)

class STSearchView(SearchView):

    template='search/index.html'

    def __init__(self, form_class=STSearchForm, *args, **kwargs):
        return super(STSearchView, self).__init__(form_class=form_class, *args, **kwargs)

    def __call__(self, request, querySetKlass=None):
        querySetKlass = querySetKlass if querySetKlass else STSearchQuerySet

        self.session = request.session
        self.request = request
        self.parse_get_args()

        if self.get_args["advanced"]:
            self.request.GET = self.request.GET.copy()
            self.request.GET['q'] = '*'
            self.searchqueryset = querySetKlass()

            condition = STSearchView.ConditionBuilder()

            if "title" in self.get_args['advanced_fields']:
                title = self.get_args['advanced_fields']['title']
                if self.get_args['title_op'] == 'OR':
                    for word in title.split():
                        condition.add({"title":word})
                else:
                    condition.add({"title":title})

            if "name" in self.get_args['advanced_fields']:
                condition.next(self.get_args['authors_op'].lower())
                authors = [name.strip() for name in self.get_args['advanced_fields']['name'].split(",")]
                for name in authors:
                    condition.add({"name":name})

            self.searchqueryset = self.searchqueryset.filter(condition.get()) if not condition.empty() else self.searchqueryset

        else:
            self.searchqueryset = querySetKlass()

        if 'orderby' in self.get_args:
            self.searchqueryset = self.searchqueryset.order_by(*self.get_args['orderby'])


        return super(STSearchView, self).__call__(request)

    class ConditionBuilder(object):

        def __init__(self):
            self.all_condition = []
            self.condition = None
            self.op = "or"

        def add(self, new_condition):
            if not self.condition:
                self.condition = SQ(**new_condition)
            elif self.op == "or":
                self.condition |= SQ(**new_condition)
            elif self.op == "and":
                self.condition &= SQ(**new_condition)
            else:
                raise Exception("Not supported operator!")

        def next(self, op="or"):
            self.op = op
            if self.condition:
                self.all_condition.append(self.condition)
                self.condition = None

        def get(self):
            self.next()
            result = reduce(lambda x,y:SQ(x)&SQ(y), self.all_condition) if len(self.all_condition) > 0 else None
            return result

        def empty(self):
            return len(self.all_condition) == 0 and self.condition == None

    def simplifyPrice(self, price_str):
        price_str = price_str.replace(',', '.')
        c = price_str.count('.')
        if c == 0:
            if price_str.isdigit():
                return int(price_str + '00')
        elif c == 1:
            length = price_str.find('.')+len('00')
            price_str=price_str.replace('.', '')
            price_str=price_str.ljust(length, '0')[:length]
            if price_str.isdigit():
                return int(price_str)

        return None

    def parse_get_args(self):
        self.get_args={}
        if "formats" in self.request.GET:
            formats = self.request.GET["formats"].split(",")
            self.get_args["formats"] = [format for format in formats if format in supported_formats_flat]

        for price_border_name in ["from", "to"]:
            if price_border_name in self.request.GET:
                value = self.simplifyPrice(self.request.GET[price_border_name])
                if value != None:
                    self.get_args[price_border_name] = value

        if "services" in self.request.GET:
            self.get_args["services"] = self.request.GET["services"].split(",")

        def replace(my_list, X, Y):
            while X in my_list:
                my_list.insert(my_list.index(X), Y)
                my_list.pop(my_list.index(X))

        if 'orderby' in self.request.GET:
            self.get_args['orderby'] = self.request.GET['orderby'].split(',')

            self.get_args['orderby'] = [orderby for orderby in self.get_args['orderby'] if orderby in ["random", "price", "-price", "title", "-title"]]
            self.get_orderby_list = list(self.get_args['orderby'])

            if "random" in self.get_args['orderby']:
                replace(self.get_args['orderby'], "random", "random"+str(random.randint(0,1000)))

            for item in [("price", "price_lowest"), ("title","sort_title")]:
                replace(self.get_args['orderby'], item[0], item[1])
                replace(self.get_args['orderby'], "-"+item[0], "-"+item[1])

        self.get_args["advanced"] = ('advanced' in self.request.GET and self.request.GET['advanced'] == 'true')

        if self.get_args['advanced']:

            self.get_args['advanced_fields'] = {}

            if 'title' in self.request.GET:
                self.get_args['advanced_fields']['title'] = self.request.GET['title']
                self.get_args['title_op'] = self.request.GET.get('title_op', 'AND')

            if 'authors' in self.request.GET:
                self.get_args['advanced_fields']['name'] = self.request.GET['authors']
                self.get_args['authors_op'] = self.request.GET.get('authors_op', 'OR')


    def pre_filtering(self):
        condition = STSearchView.ConditionBuilder()

        if "formats" in self.get_args:
            for format in self.get_args["formats"]:
                condition.add({"format_" + format:True})

        condition.next("and")

        if "from" in self.get_args:
            condition.add({"price__gte":self.get_args["from"]})

        if "to" in self.get_args:
            condition.add({"price__lte":self.get_args["to"]})

        condition.next("or")

        if "services" in self.get_args:
            for service in self.get_args["services"]:
                condition.add({"bookstore":service})
        return condition

    def get_results(self):
        condition = self.pre_filtering()
        results = self.form.search() if condition.empty() else self.form.search().filter(condition.get())

        results.get_args = self.get_args
        return results

    def getServicesInfo(self):
        results = STSearchQuerySet().using('bookstore').auto_query("bookstores").load_all()
        bookstores=[]
        for result in results:
            bs = {}
            bs['name'] = result.bookstore
            bs['name_lowercase'] = result.bookstore.lower()
            bs['miniBookCount'] = result.miniBookCount
            bookstores.append(bs)

        return bookstores

    def extra_context(self):
        extra = super(STSearchView, self).extra_context()

        self.servicesInfo = self.getServicesInfo()

        extra['top_menu'] = getListOfTopMenuServices(self.request)
        extra['supported_formats'] = supported_formats
        extra["prefix"] = "s"

        self.load_values_if_exists_in_session(extra, ['isMenuHidden'])

        extra['filters'] = [
                                {
                                    'name':'FORMATY',
                                    'name_id':'formats',
                                    'template_file':'filter/bullet_list.html',
                                    'data':self.loadFilterState(supported_formats, "formats")
                                },
                                {
                                    'name':'CENA',
                                    'name_id':'price',
                                    'template_file':'filter/price.html',
                                    'data':self.loadFilterPriceState(['from', 'to'])
                                },
#                                {
#                                    'name':'OZNACZENIA',
#                                    'name_id':'formats',
#                                    'template_file':'filter/bullet_list.html',
#                                    'data':self.loadFilterState({'Wszystkie':["Promocje", "Nowości", "Bestsellery"]}, "special")
#                                },
                                {
                                    'name':'SERWISY',
                                    'name_id':'services',
                                    'template_file':'filter/bullet_list.html',
                                    'data':self.loadFilterState({'Wszystkie':[bookstore['name'] for bookstore in self.servicesInfo]}, "services")

                                },
 #                               {
 #                                   'name':'SPOSÓB PŁATNOŚCI',
 #                                   'name_id':'formats',
 #                                   'template_file':'filter/bullet_list.html',
 #                                   'data':self.loadFilterState({"Przez serwis":["DotPay", "ePrzelewy", "PayU", "Przelewy24.pl", "transferuj.pl", "YetiPay", "mPay", "SkyCash", "SMS", "PayPal", "karty płatnicze", "Przelewy24.pl"]}, "formats")
#                                },
                        ]

        if self.get_args.get('orderby'):
            extra['orderby'] = self.get_orderby_list

        if self.get_args.get('advanced'):
            extra['advanced'] = "true"

        authorization(self.request, extra)

        return extra

    def load_values_if_exists_in_session(self, extra_dict, values):
        for value in values:
            if value in self.request.session:
                extra_dict[value] = self.request.session[value]

    def loadFilterPriceState(self, borders):
        dic = {}
        for border in borders:
            if border in self.get_args:
                dic["price_" + border] = str("%.2f" % (self.get_args[border]/100.0))
        return dic

    def loadFilterState(self, dic, name):
        get = self.get_args[name] if name in self.get_args else []
        r = []
        for group_name, group_item_list in dic.items():
            r.append({"name":group_name, "items":[ {'name':item, 'isFilterActive':(item in get)} for item in group_item_list]})
        return r

class STSearchQuerySet(SearchQuerySet):

    def convertResultsToProducts(self, results):
        products=[]
        for product in results:
            product.records = []

            mapping = {
                "price": product.price,
                "bookstore": product.bookstore,
                "url": product.url,
                "cover": product.cover,
                "format_mobi": product.mini_format_mobi,
                "format_pdf": product.mini_format_pdf,
                "format_epub": product.mini_format_epub,
                "format_cd": product.mini_format_cd,
                "format_mp3": product.mini_format_mp3,
                "format_ks": product.mini_format_ks,
            }

            records_in_products = len(product.price)

            for i in range(records_in_products):
                record = {}
                for key, list_of_values in mapping.items():
                    record[key] = list_of_values[i]

                record["formats"] = [
                    attr.replace("format_", "")
                    for attr, value in record.iteritems()
                    if str(attr).startswith("format_") and value
                ]

                record["id"] = str(product.id) + '-' + record['bookstore']
                product.records.append(record)

            # TODO: temporary solution
            if product.name:
                product.name = set(product.name)

            products.append(product)

        return products

    def pre_process_records(self, products):
        for product in products:
            min = product.records[0]['price']
            for record in product.records:
                if record['price'] < min:
                    min = record['price']

            product.price_lowest_before_filtering = str("%.2f" % (min/100.0))
        return products

    def post_process_records(self, products):
        for product in products:
            min = product.records[0]['price'] #we do not need check if element exist, because empty products were excluded earlier
            formats=set()
            services=set()
            for record in product.records:
                if record['price'] < min:
                    min = record['price']
                record['price'] = str("%.2f" % (int(record['price'])/100.0))
                formats |= set(record['formats'])
                services.add(record['bookstore'])

            product.formats = formats
            product.price_lowest = str("%.2f" % (min/100.0))
            product.services = services
            product.cover = next((record["cover"] for record in product.records if record["cover"] != ""), "")
        return products

    def post_filtering(self, products):

        filtered_products = []

        for product in products:
            filtered_records = list(product.records)

            ### start of filtering records ###

            if "formats" in self.get_args:
                filtered_records = [record for record in filtered_records if any(record["format_" + format] for format in self.get_args["formats"])]

            if "from" in self.get_args:
                filtered_records = [record for record in filtered_records if record['price'] >= self.get_args["from"]]

            if "to" in self.get_args:
                filtered_records = [record for record in filtered_records if record['price'] <= self.get_args["to"]]

            if "services" in self.get_args:
                filtered_records = [record for record in filtered_records if record['bookstore'] in self.get_args["services"]]

            ### end of filtering records ###

            product.filtered_formats = []
            for record in product.records:
                if not record in filtered_records:
                    for format in record["formats"]:
                        if not format in product.filtered_formats:
                            product.filtered_formats.append(format)

            product.filtered_records_number = len(product.records) - len(filtered_records)

            product.records = filtered_records

            if len(product.records) != 0:
                filtered_products.append(product)

        return filtered_products


    def _fill_cache(self, start, end, **kwargs):
        self.query._reset()

        needed = end - start
        ac = 0

        cache_container = []

        while needed != ac:

            s_start = start + self.filtered_offset + ac
            s_end   = start + self.filtered_offset + ac + (needed - ac)

            self.query.set_limits(s_start, s_end)
            results = self.query.get_results(**kwargs)
            c = self.query.get_count()

            if results == None or len(results) == 0:
                return False

            if len(self._result_cache) == 0:
                self._result_cache = [None for i in xrange(c)]

            #if start is None:
            #    start = 0

            #if end is None:
            #    end = self.query.get_count()

            to_cache = self.post_process_results(results)
            filtered = len(results) - len(to_cache)

            self.filtered_offset += filtered
            for i in range(filtered):
                del self._result_cache[-1]

            ac += len(to_cache)

            cache_container += to_cache

            if s_end >= c:
                break


        self._result_cache[start:start + ac] = cache_container

        return True


    def post_process_results(self, results):
        if self.query._using in ['default', 'book_details']:
            results = self.convertResultsToProducts(results)
            results = self.pre_process_records(results)
            results = self.post_filtering(results)
            results = self.post_process_records(results)

        return results

    def __init__(self, using=None, query=None):
        self.filtered_offset = 0
        return super(STSearchQuerySet, self).__init__(using, query)

    def order_by(self, *args):
        clone = self.clear_order_by()
        for field in args:
            clone.query.add_order_by(field)

        return clone

    def clear_order_by(self):
        clone = self._clone()
        clone.query.clear_order_by()
        return clone

def hide_menu(request, value):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    request.session['isMenuHidden'] = bool(int(value))

    return HttpResponse('ok')
