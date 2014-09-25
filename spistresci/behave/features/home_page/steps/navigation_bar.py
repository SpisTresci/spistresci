from behave import *


@given('I am on home page')
def step_impl(context):
    context.selenium.home_page.base.go_to_home_page()


@when("service name in navigation bar match current service name")
def step_impl(context):
    context.selenium.navigation_bar.\
        service_name_in_navbar_match_current_service()


@then('service name in navigation bar is marked as active')
def step_impl(context):
    context.selenium.navigation_bar.check_marked_as_active_services()
