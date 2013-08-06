from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from spistresci.forms import RegistrationForm
from _constants import *

def register_user(request, template = 'register.html'):
    c = {'top_menu':list_of_services}
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

    return render_to_response(template, c)

def egazeciarz_register_user(request):
    return register_user(request, 'egazeciarz_register.html')
