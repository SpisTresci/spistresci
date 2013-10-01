# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from spistresci.auth.views import authorization
from spistresci.constants import *
from constants import *

def book(request, book_id):
    c = {'top_menu':getListOfTopMenuServices(request)}
    c.update({'path':request.path})
    authorization(request, c)
    c['request'] = request


    return render_to_response('book.html', c)
