Feature: User search

    Scenario: Add a user and then search for them
        Given I open "/web_user_search/new"
        Then I should see the heading "Add User"
        When I fill in "name" with "Geoff Bache" and submit to url "/web_user_search/new"
        Then I should see "Successfully added user"
        Given I open "/web_user_search/search"
        When I fill in "search" with "Geoff" and submit the form to url "/web_user_search/search"
        Then I should see "result(s) found"
        Then I should see "Geoff Bache"

