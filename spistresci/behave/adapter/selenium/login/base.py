from django.core.urlresolvers import reverse_lazy
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class LoginBaseSeleniumAdapter(BaseSeleniumAdapter):
    url = reverse_lazy('account_login')
