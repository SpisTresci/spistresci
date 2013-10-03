# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from spistresci.auth.views import authorization
from spistresci.constants import *
from constants import *

def book(request, book_id):
    c = {'top_menu':getListOfTopMenuServices(request)}
    c.update({'path':request.path})
    authorization(request, c)
    c['request'] = request
    c['book'] = get_book(book_id)


    return render_to_response('book.html', c)

def book_description(request, book_id):
    return HttpResponse(get_book_description(book_id))

def get_book(book_id):
    #TODO: we have only 3 random books now.
    import random
    book_id = random.choice(['kilka', 'szkolne', 'aby'])
    return books.get(book_id, {})

def get_book_description(book_id):
    #TODO: we have only 3 random books now.
    import random
    book_id = random.choice(['kilka', 'szkolne', 'aby'])
    return book_descriptions[book_id]