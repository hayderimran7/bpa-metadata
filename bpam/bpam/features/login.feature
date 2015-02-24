Feature: Login

  Scenario: You are on login page
    Given I go to "/admin"
    Then I should see "bpa-metadata"

  Scenario: Login successful as admin
    Given I go to "/admin"
    Then I log in as "admin" with "admin" password expects "Bioplatforms Australia Metadata"
    And I click "Log out"
