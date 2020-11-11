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

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "First_Name" to "Lady"
    And I set the "Last_Name" to "Gaga"
    And I set the "Email" to "ladygaga@gmail.com"
    And I set the "Address" to "888 Brooklyn St"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "First_Name" field should be empty
    And the "Last_Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Lady" in the "First_Name" field
    And I should see "Gaga" in the "Last_Name" field
    And I should see "ladygaga@gmail.com" in the "Email" field
    And I should see "888 Brooklyn St" in the "Address" field
    And I should see "True" in the "Active" dropdown

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I press the "search" button
    And I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    When I press the "Retrieve" button
    Then I should see the message "404 Not Found: Customer with the id was not found."

# Scenario: Suspend a Customer
# When I visit the "Home Page"
# And I press the "search" button
# And I copy the "Id" field
# And I press the "Clear" button
# And I paste the "Id" field
# And I press the "Delete" button
# Then I should see the message "Customer has been Deleted!"
# When I press the "Retrieve" button
# Then I should see the message "404 Not Found"