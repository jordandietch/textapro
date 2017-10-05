from datetime import datetime, timedelta
from behave import *
from models import Lead
from app import message_response

use_step_matcher("re")


@given("a homeowner is on the homepage")
def step_impl(context):
    context.page = context.client.get('/')
    assert context.page.status_code == 200
    assert context.page
    assert context.db


@when("they submit the text a pro form with a valid phone number")
def step_impl(context):
    context.good_telephone = context.test_phone
    lead = Lead.query.filter_by(telephone=context.good_telephone).first()
    assert lead is None
    context.page = context.client.post('/', data=dict(
        telephone=context.good_telephone
    ), follow_redirects=True)


@then("send a text message and an email to a pro and redirect to a thank you page")
def step_impl(context):
    assert b'Thank You' in context.page.data


@step("show an error message if an invalid phone number is input")
def step_impl(context):
    context.page = context.client.post('/', data=dict(
        telephone='+1805abcdefg'
    ), follow_redirects=True)
    assert b'Please enter a valid phone number.' in context.page.data


@step("phone number gets saved to the database")
def step_impl(context):
    lead = Lead.query.filter_by(telephone=context.good_telephone).first()
    print(lead)
    assert lead is not None


@step("same phone number can't submit a text twice through form")
def step_impl(context):
    context.page = context.client.post('/', data=dict(
        telephone=context.good_telephone
    ), follow_redirects=True)
    assert b'Thank you for submitting. Please check your phone.' in context.page.data


@step("same phone number will not get saved to the database twice")
def step_impl(context):
    leads = Lead.query.filter_by(telephone=context.good_telephone).all()
    assert len(leads) == 1


@given("a homeowner has the text a pro number")
def step_impl(context):
    context.page = context.client.get('/pro-response')
    assert context.page.status_code == 200
    assert context.page


@when("they send their first text")
def step_impl(context):
    context.first_text_already_sent = context.message_response(context.test_phone)


@then("send the homeowner a text asking them to confirm their phone number")
def step_impl(context):
    assert 'Text Yes to verify your phone number so that we can connect you with a contractor, or No to cancel' not in context.first_text_already_sent[0]


@given("a homeowner wants to respond after 7 days")
def step_impl(context):
    lead = Lead.query.filter_by(telephone=context.test_phone).first()
    eight_days_ago = datetime.now() - timedelta(days=8)
    lead.received_on = eight_days_ago
    context.db.session.add(lead)
    context.db.session.commit()


@when("they send a text more than 7 days after their original text")
def step_impl(context):
    context.eight_day_old_lead = context.message_response(context.test_phone)


@then("send the homeowner a text letting them know we are matching them with a contractor")
def step_impl(context):
    assert 'Hold tight. We are in the process of connecting you with a contractor.' in context.eight_day_old_lead[0]


@given("a homeowner wants to confirm their phone number")
def step_impl(context):
    lead = Lead.query.filter_by(telephone=context.test_phone).first()
    lead.received_on = datetime.now()
    context.db.session.add(lead)
    context.db.session.commit()


@when("they respond back to confirm their phone number")
def step_impl(context):
    context.confirming_phone = context.message_response(context.test_phone, 'Yes')


@then("message them again letting them know we will now match them")
def step_impl(context):
    assert 'Thanks for verifying your number. We will connect you with a contractor shortly' in context.confirming_phone[0]


@given("a homeowner has already confirmed their phone number")
def step_impl(context):
    context.homeowner_response = 'No'


@when("they respond back to cancel")
def step_impl(context):
    context.not_cancelling_matching_process = context.message_response(context.test_phone, context.homeowner_response)


@then("don't message them again")
def step_impl(context):
    assert context.not_cancelling_matching_process[0] is None


@given("a homeowner has not already confirmed their phone number")
def step_impl(context):
    lead = Lead.query.filter_by(telephone=context.test_phone).first()
    lead.is_verified = False
    context.db.session.add(lead)
    context.db.session.commit()


@when('they respond back with "no"')
def step_impl(context):
    context.cancelling_matching_process = context.message_response(context.test_phone, 'No')


@then("message them to let them know we are cancelling their request")
def step_impl(context):
    assert 'Ok we\'ve cancelled your request' in context.cancelling_matching_process[0]