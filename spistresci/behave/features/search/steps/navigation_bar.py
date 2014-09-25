from behave import *


@given('I am on search page')
def step_impl(context):
    context.selenium.search.base.go_to_search_page()


@when("service_ name in navigation bar match current service name")
def step_impl(context):
    context.selenium.navigation_bar.\
        service_name_in_navbar_match_current_service()


@then('service_ name in navigation bar is marked as active')
def step_impl(context):
    context.selenium.navigation_bar.check_marked_as_active_services()
