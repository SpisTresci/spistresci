from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class HomePageBaseSeleniumAdapter(BaseSeleniumAdapter):

    def go_to(self):
        self.browser.get(self.base_url)