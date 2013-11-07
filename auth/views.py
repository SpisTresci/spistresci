from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from spistresci.auth.forms import UserForm

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


class BaseUserView(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(BaseUserView, self).dispatch(request, *args, **kwargs)


class Profile(BaseUserView, UpdateView):

    form_class = UserForm
    template_name = 'auth/profile.html'

    def get_object(self, *args, **kwargs):
        self.success_url = reverse('profile:home')
        return self.user
