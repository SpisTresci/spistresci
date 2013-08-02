# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def index(request):
    c = {}
    c['navwrap_list']= [
        {
            "label":"Strona Główna",
            "url":"/"
        },
        {
            "label":"Zaloguj",
            "url":"/accounts/login/"
        },
        {
            "label":"Zarejestruj",
            "url":"/accounts/register/"
        },
    ]
    c['path'] = request.path
    return render_to_response('index.html', c)