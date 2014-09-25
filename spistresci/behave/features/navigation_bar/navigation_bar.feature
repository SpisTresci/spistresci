Feature: Search Page Navigation Bar

  Scenario Outline: Active service is marked on ...
    Given I am on <page name>
     When service name in navigation bar match current service name
     Then service name in navigation bar is marked as active

  Examples: Page Name
    | page name     |
    | home page     |
    | search page   |
    | login page    |
    | partners page |
    | about us page |
