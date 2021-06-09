from django.core.urlresolvers import reverse_lazy
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class ContactBaseSeleniumAdapter(BaseSeleniumAdapter):
    url = reverse_lazy('contact')
