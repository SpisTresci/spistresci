# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.detail import DetailView
from spistresci.models import MasterBook
from spistresci.search.forms import SpisTresciSearchForm

class STBookView(DetailView):
    model = MasterBook

    def get_context_data(self, **kwargs):
        context = super(STBookView, self).get_context_data(**kwargs)
        context['form'] = SpisTresciSearchForm
        return context

def book_redirect(request):
    return render(request, "book/redirect.html", request.GET)
