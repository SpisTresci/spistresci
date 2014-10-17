import os
from selenium import webdriver

from spistresci.behave.adapter.selenium.about_us.base import \
    AboutUsBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.book.base import \
    BookBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.contact.base import \
    ContactBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.home_page.base import \
    HomePageBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.login.base import \
    LoginBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.partners.base import \
    PartnersBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.profile.base import \
    ProfileBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.register.base import \
    RegisterBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.search.base import \
    SearchBaseSeleniumAdapter

from spistresci.behave.adapter.selenium.terms_of_use.base import \
    TermsOfUseBaseSeleniumAdapter


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
    # context._selenium_driver.get(context.base_url)

    # Selenium adapters
    context.selenium = Placeholder()

    context.selenium.about_us = Placeholder()
    context.selenium.about_us.base = AboutUsBaseSeleniumAdapter(context)

    context.selenium.book = Placeholder()
    context.selenium.book.base = BookBaseSeleniumAdapter(context)

    context.selenium.contact = Placeholder()
    context.selenium.contact.base = ContactBaseSeleniumAdapter(context)

    context.selenium.home_page = Placeholder()
    context.selenium.home_page.base = HomePageBaseSeleniumAdapter(context)

    context.selenium.search = Placeholder()
    context.selenium.search.base = SearchBaseSeleniumAdapter(context)

    context.selenium.login = Placeholder()
    context.selenium.login.base = LoginBaseSeleniumAdapter(context)

    context.selenium.partners = Placeholder()
    context.selenium.partners.base = PartnersBaseSeleniumAdapter(context)

    context.selenium.profile = Placeholder()
    context.selenium.profile.base = ProfileBaseSeleniumAdapter(context)

    context.selenium.register = Placeholder()
    context.selenium.register.base = RegisterBaseSeleniumAdapter(context)

    context.selenium.search = Placeholder()
    context.selenium.search.base = SearchBaseSeleniumAdapter(context)

    context.selenium.terms_of_use = Placeholder()
    context.selenium.terms_of_use.base = TermsOfUseBaseSeleniumAdapter(context)


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