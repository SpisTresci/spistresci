import urlparse
from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class AboutUsBaseSeleniumAdapter(BaseSeleniumAdapter):

    def go_to(self):
        self.browser.get(urlparse.urljoin(self.base_url, 'about-us/'))