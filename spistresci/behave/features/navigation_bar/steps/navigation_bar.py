from behave import *


@given('I am on home page')
def step_impl(context):
    context.selenium.home_page.base.go_to()


@given('I am on search page')
def step_impl(context):
    context.selenium.search.base.go_to()


@given('I am on login page')
def step_impl(context):
    context.selenium.login.base.go_to()


@given('I am on partners page')
def step_impl(context):
    context.selenium.partners.base.go_to()


@given('I am on about us page')
def step_impl(context):
    context.selenium.about_us.base.go_to()


@when("service name in navigation bar match current service name")
def step_impl(context):
    context.selenium.navigation_bar.\
        service_name_in_navbar_match_current_service()


@then('service name in navigation bar is marked as active')
def step_impl(context):
    context.selenium.navigation_bar.check_marked_as_active_services()
