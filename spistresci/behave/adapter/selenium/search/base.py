import urlparse
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class SearchBaseSeleniumAdapter(BaseSeleniumAdapter):

    def go_to_search_page(self):
        self.browser.get(urlparse.urljoin(self.base_url, 'search/'))