"""
Customer Steps
Steps file for Customers.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""

from os import getenv
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

@given('the following customers')
def step_impl(context):
    """ Delete all Customers and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/customers/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/customers'
    for row in context.table:
        data = {
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "email": row['last_name'],
            "address": row['address'],
            "active": row['active'] in ['True', 'true', '1']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@when(u'I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    # context.resp = context.app.get('/')
    context.driver.get(context.base_url)


@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    # assert message in str(context.resp.data)
    expect(context.driver.title).to_contain(message)


@then(u'I should not see "{message}"')
def step_impl(context, message):
    # assert message not in str(context.resp.data)
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then('I should see "{name}" in the results')
def step_impl(context, name):
    # element = context.driver.find_element_by_id('search_results')
    # expect(element.text).to_contain(name)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)