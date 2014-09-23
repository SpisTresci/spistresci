Feature: Home Page Navigation Bar

  Scenario: Active service is marked
    Given I am on home page
     When service name in navigation bar match current service name
     Then service name in navigation bar is marked as active

  Scenario: Login option available on home page
    Given I am on home page
     When I am not logged in
     Then Login option is available

  Scenario: Logout option available on home page
    Given I am on home page
     When I am logged in
     Then Logout option is available