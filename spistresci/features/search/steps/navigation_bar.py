from behave import *

import urlparse


@given('I am on search page')
def step_impl(context):
    context.driver.get(urlparse.urljoin(context.base_url, 'search/'))


@when("service_ name in navigation bar match current service name")
def step_impl(context):
    menu = context.driver.find_element_by_xpath("//ul[@class='menu']")

    a_elements = menu.find_elements_by_xpath(
        "li[not(contains(@class, 'menu2'))]/a"
    )

    context.data = {
        'marked_as_active': [],
    }

    for a in a_elements:
        if a.get_attribute('href') in context.driver.current_url:
            context.data['marked_as_active'].append(a)


@then('service_ name in navigation bar is marked as active')
def step_impl(context):

    for item in context.data['marked_as_active']:
        li_element = item.find_element_by_xpath('..')
        assert li_element.get_attribute('class'), 'act'