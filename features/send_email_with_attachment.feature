Feature: Send email with attachment via Outlook

  As an email user
  I want to send an email with an attachment to a contact
  So that the recipient receives my message and file

  Scenario: Send an email with attachment to a saved contact and logout
    Given the user is on the Outlook login page
    When the user logs in with valid credentials
    Then the inbox should be displayed

    When the user composes a new email
    And the user adds recipient "Test" from contacts
    And the user enters the subject "Test Automation Task"
    And the user enters the body "This email was sent by an automated test."
    And the user attaches the file "test_attachment.txt"
    And the user sends the email
    Then the email should be sent successfully
    And the inbox should receive an email with subject "Test Automation Task"

    When the user logs out
    Then the login page should be displayed
