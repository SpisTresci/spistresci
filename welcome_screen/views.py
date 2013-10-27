# -*- coding: utf-8 -*-
# from django.template.loader import POST_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from application.models import Address
from datetime import datetime
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
import os


def main(request):
    if request.method == 'POST' and '@' in request.POST['mail'] and not(Address.objects.filter(email=request.POST['mail']).exists()):
        addr = request.POST['mail']
        dat = datetime.now()
        new_email = Address(email=addr, date=dat)
        new_email.save()
        context = {'response': "Dziękujemy za pozostawienie adresu e-mail."}
    else:
        context = {'response': ""}
    return render(request, 'template.html', context)

#Note: This seems to be stupid, but in production this should be absolute path
#Moreover defining separate view for each image looks bad in my opinion
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
def logo(request):
    image_data = open(os.path.join(SITE_ROOT,'../imgs/Logo_ST.png'), "rb").read()
    return HttpResponse(image_data, mimetype="image/png")

