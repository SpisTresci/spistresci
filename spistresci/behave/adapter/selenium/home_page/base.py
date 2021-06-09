from django.core.urlresolvers import reverse_lazy
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class HomePageBaseSeleniumAdapter(BaseSeleniumAdapter):
    url = reverse_lazy('index')
