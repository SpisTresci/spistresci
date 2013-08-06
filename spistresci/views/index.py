from django.shortcuts import render_to_response
from auth import authorization
from _constants import *

def index(request):
    c = {'top_menu':list_of_services}
    c.update({'path':request.path})
    authorization(request, c)
    c['request'] = request
    return render_to_response('index.html', c)
