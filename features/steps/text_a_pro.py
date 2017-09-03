from behave import *
from models import Lead

use_step_matcher("re")


@given("a homeowner is on the homepage")
def step_impl(context):
    context.page = context.client.get('/')
    assert context.page.status_code == 200
    assert context.page
    assert context.db


@when("they submit the text a pro form with a valid phone number")
def step_impl(context):
    context.good_telephone = '+18059011596'
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
        telephone='+1805901159b'
    ), follow_redirects=True)
    assert b'Please enter a valid phone number.' in context.page.data


@step("phone number gets saved to the database")
def step_impl(context):
    lead = Lead.query.filter_by(telephone=context.good_telephone).first()
    assert lead is not None


@step("same phone number can't submit a text twice through form")
def step_impl(context):
    context.page = context.client.post('/', data=dict(
        telephone=context.good_telephone
    ), follow_redirects=True)
    assert b'Thank you for submitting. A contractor will reach out shortly.' in context.page.data


@step("same phone number will not get saved to the database twice")
def step_impl(context):
    leads = Lead.query.filter_by(telephone=context.good_telephone).all()
    assert len(leads) == 1


@given("a homeowner has the text a pro number")
def step_impl(context):
    context.page = context.client.get('/pro-response')
    assert context.page.status_code == 200
    assert context.page


@when("they send a text")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("send a text to the admins")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("send an email to the admins")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass