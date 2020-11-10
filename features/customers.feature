Feature: The customer service back-end
    As a online store
    I need a RESTful customer service
    So that I can keep track of all my customer accounts

Background:
    Given the following customers
        | first_name    | last_name   | email          | address            | active    |
        | Nick          | Vardaro     | nvar@gnyu.edu  | 123 Brooklyn Ave   | True      |
        | Henry         | Ou          | hou@nyu.edu    | 888 Brooklyn St    | True      |
        | Justin        | Chiang      | jchi@gmail.com | 888 Brooklyn St    | True      |
        | Rohan         | Raj         | rraj@gmail.com | 888 Brooklyn St    | False     |
        | Nancy         | Wen         | nwen@gmail.com | 100 Main St        | False     |


Scenario: The server is running
    When I visit the "home page"
    Then I should see "Customer Demo RESTful Service" in the title
    And  I should not see "404 Not Found"

Scenario: List all customers
    When I visit the "home page"
    And I press the "search" button
    Then I should see "Nick" in the results
    And I should see "Henry" in the results
    And I should see "Justin" in the results
    And I should see "Rohan" in the results
    And I should see "Nancy" in the results