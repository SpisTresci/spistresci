import urlparse

class BaseSeleniumAdapter(object):

    url = None

    def __init__(self, context):
        self.browser = context._selenium_driver
        self.base_url = context.base_url

    def go_to(self):
        if not self.url:
            raise NotImplementedError("Please define url for page")

        url = (self.base_url + unicode(self.url)).replace('//', '/')
        self.browser.get(url)
