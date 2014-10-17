from django.core.urlresolvers import reverse_lazy
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class BookBaseSeleniumAdapter(BaseSeleniumAdapter):
    url = reverse_lazy('book_page')
