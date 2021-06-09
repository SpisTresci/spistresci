from django.core.urlresolvers import reverse_lazy
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class TermsOfUseBaseSeleniumAdapter(BaseSeleniumAdapter):
    url = reverse_lazy('terms_of_use')
