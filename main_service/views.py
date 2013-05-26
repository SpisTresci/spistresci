# -*- coding: utf-8 -*-
# from django.template.loader import POST_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
import os


def index(request):
    return render_to_response('index.html')

def search(request):
    return render_to_response('search.html')