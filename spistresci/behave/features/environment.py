import os
from selenium import webdriver


from spistresci.behave.adapter.selenium.navigation_bar import (
    NavigationBarSeleniumAdapter,
)

from spistresci.behave.adapter.selenium.home_page.base import (
    HomePageBaseSeleniumAdapter,
)

from spistresci.behave.adapter.selenium.search.base import (
    SearchBaseSeleniumAdapter,
)


class Placeholder(object):
    pass


def before_all(context):
    context.base_url = os.environ.get('ST_URL')
    context.driver = webdriver.Chrome()

    adapter_type = os.environ.get('ADAPTER_TYPE', 'selenium')
    context.base_url = _get_st_url(os.environ.get('ST_URL'))
    context._selenium_driver = _get_selenium(os.environ.get('BROWSER'))
    context._selenium_driver.set_page_load_timeout(30)
    context._selenium_driver.set_window_size(1400, 1000)
    context._selenium_driver.get(context.base_url)

    # Selenium adapters
    context.selenium = Placeholder()

    context.selenium.navigation_bar = NavigationBarSeleniumAdapter(context)

    context.selenium.home_page = Placeholder()
    context.selenium.home_page.base = HomePageBaseSeleniumAdapter(context)

    context.selenium.search = Placeholder()
    context.selenium.search.base = SearchBaseSeleniumAdapter(context)

def after_all(context):
    context._selenium_driver.close()


def _get_selenium(browser_type=None):
    browser_type = browser_type or 'PhantomJS'
    working_browser_types = ['PhantomJS', 'Chrome', 'Firefox']
    assert browser_type in working_browser_types, (
        'Unknown browser type {}, please use one of these with correct '
        'capitalization: {}'
    ).format(
        browser_type, ', '.join(working_browser_types)
    )
    return getattr(webdriver, browser_type)()


def _get_st_url(st_url=None):
    return st_url