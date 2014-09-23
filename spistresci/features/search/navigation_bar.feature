Feature: Search Page Navigation Bar

  Scenario: Active service is marked on Search page
    Given I am on search page
     When service_ name in navigation bar match current service name
     Then service_ name in navigation bar is marked as active
