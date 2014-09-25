class BaseSeleniumAdapter(object):

    def __init__(self, context):
        self.browser = context._selenium_driver
        self.base_url = context.base_url
