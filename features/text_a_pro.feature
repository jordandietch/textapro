# Created by jordandietch at 8/16/17
Feature: #Enter feature name here
  # Enter feature description here

  Scenario: # Enter scenario name here
    # Enter steps here
    Given a homeowner is on the homepage
    When they submit the text a pro form with a valid phone number
    Then send a text message and an email to a pro and redirect to a thank you page
    And show an error message if an invalid phone number is input
    And phone number gets saved to the database
    And same phone number can't submit a text twice through form
    And same phone number will not get saved to the database twice

  Scenario: # Enter scenario name here
    # Enter steps here
    Given a homeowner has the text a pro number
    When they send their first text
    Then send the homeowner a text asking them to confirm their phone number

  Scenario: # Enter scenario name here
    # Enter steps here
    Given a homeowner wants to respond after 7 days
    When they send a text more than 7 days after their original text
    Then send the homeowner a text letting them know we are matching them with a contractor

  Scenario: # Enter scenario name here
    # Enter steps here
    Given a homeowner wants to confirm their phone number
    When they respond back to confirm their phone number
    Then message them again letting them know we will now match them

  Scenario: # Enter scenario name here
    # Enter steps here
    Given a homeowner has already confirmed their phone number
    When they respond back to cancel
    Then don't message them again

  Scenario: # Enter scenario name here
    # Enter steps here
    Given a homeowner has not already confirmed their phone number
    When they respond back with "no"
    Then message them to let them know we are cancelling their request