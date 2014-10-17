from django.core.urlresolvers import reverse_lazy
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class AboutUsBaseSeleniumAdapter(BaseSeleniumAdapter):
    url = reverse_lazy('about_us')
