#-*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response

def main(request):
	return render_to_response('template.html',{'address': "TEST"})
 
def logo(request):
    image_data = open("/home/anni/Pulpit/djcode/mysite/imgs/Logo_ST.png", "rb").read()
    return HttpResponse(image_data, mimetype="image/png") 

"""def info(request):
    t = get_template('template.html')
    html = t.render(Context({'address': "TEST"}))
    return HttpResponse(html)
"""



