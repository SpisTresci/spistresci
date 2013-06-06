# Create your views here.
# -*- coding: utf-8 -*-
# from django.template.loader import POST_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from logos_stripe.models import bookshop
import os


def main(request):
	#p = bookshop(name="patrons2.png", address="www.publio.pl")
        #p.save();
		all=bookshop.objects.all()
		logos=({'name':"img/patrons2.png",'address':'www.publio.pl'})
		return render_to_response('templ.html', {'resp':logos,'all':all})
		
