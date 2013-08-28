from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

def authorization(request, c):
    c.update(csrf(request))

    if not request.user.is_authenticated():
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

    c.update({'user': request.user})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def accounts_social_signup(request):
    return HttpResponseRedirect('/')

def accounts_profile(request):
    return HttpResponseRedirect('/')
