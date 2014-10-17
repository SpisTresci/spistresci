Feature: Search Page Navigation Bar

  Scenario Outline: Active service is marked in navbar on specified page
    Given I am on <page name> page
     When service name in navigation bar match current service name
     Then service name in navigation bar is marked as active

  Examples: Page Name
    | page name     |
    | about us      |
    | book          |
    | contact       |
    | home          |
    | login         |
    | partners      |
    | profile       |
    | register      |
    | search        |
    | terms of use  |
