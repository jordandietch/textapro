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
    When they send a text
    Then send a text to the admins
    And send an email to the admins