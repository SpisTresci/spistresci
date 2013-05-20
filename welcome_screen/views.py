# -*- coding: utf-8 -*-
# from django.template.loader import POST_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from application.models import Address
from datetime import datetime
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect


def main(request):
    if request.method == 'POST' and '@' in request.POST['mail'] and not(Address.objects.filter(email=request.POST['mail']).exists()):
        addr = request.POST['mail']
        dat = datetime.now()
        new_email = Address(email=addr, date=dat)
        new_email.save();
        return render_to_response('template.html', {'response': "Dziękujemy za pozostawienie adresu e-mail."})
    else:
        return render_to_response('template.html', {'response':""})

def logo(request):
    image_data = open("imgs/Logo_ST.png", "rb").read()
    return HttpResponse(image_data, mimetype="image/png") 

