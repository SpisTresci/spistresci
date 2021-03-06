from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from spistresci.forms import RegistrationForm
from spistresci.constants import *

def register_user(request, template = 'register.html'):
    c = {'top_menu':getListOfTopMenuServices(request)}
    c.update({'path':request.path})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
    else:
        form = RegistrationForm()

    c.update(csrf(request))

    c['form'] = form
    c['request'] = request

    return render(request, template, c)

def egazeciarz_register_user(request):
    return register_user(request, 'egazeciarz_register.html')
