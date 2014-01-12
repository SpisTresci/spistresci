from spistresci.search.views import STSearchQuerySet
from django.shortcuts import render_to_response
from spistresci.constants import *
from spistresci.auth.views import authorization

def partners(request):
    c = {'top_menu':getListOfTopMenuServices(request)}
    c.update({'path':request.path})
    authorization(request, c)
    c['request'] = request

    results = STSearchQuerySet().using('bookstore').auto_query("bookstores").load_all()
    c['services']=[]
    for result in results:
        bs = {}
        bs['name_lowercase'] = result.bookstore.lower()
        bs['website'] = 'http://pajacyk.pl/' #result.bookstore.lower()
        c['services'].append(bs)

    return render_to_response('partners.html', c)
