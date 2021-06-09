from django.core.urlresolvers import reverse_lazy
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class RegisterBaseSeleniumAdapter(BaseSeleniumAdapter):
    url = reverse_lazy('account_signup')
