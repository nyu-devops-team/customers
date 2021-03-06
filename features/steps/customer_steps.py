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
import time
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))
ID_PREFIX = 'customer_'

@given('the following customers')
def step_impl(context):
    """ Delete all Customers and load new ones """
    headers = {'Content-Type': 'application/json'}

    context.resp = requests.get(context.base_url + '/customers', headers=headers)
    expect(context.resp.status_code).to_equal(200)

    # clear the customer table
    for customer in context.resp.json():
        context.resp = requests.delete(context.base_url + '/customers/' + str(customer["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)

    # load database with new customers
    create_url = context.base_url + '/customers'
    for row in context.table:
        data = {
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "email": row['email'],
            "address": row['address'],
            "active": row['active'] in ['True', 'true', '1']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)
    time.sleep(1)


@when(u'I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    time.sleep(1)


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
    time.sleep(1)

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)
    time.sleep(1)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)
    time.sleep(1)


@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute('value')).to_be(u'')

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower()
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    expect(element.first_selected_option.text).to_equal(text)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)
    time.sleep(1)

@then('I should see all customers with "{text_string}" in the results')
def step_impl(context, text_string):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            text_string
        )
    )
    expect(found).to_be(True)   

@then('I should not see "{text_string}" in the results')
def step_impl(context, text_string):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (text_string, element.text)
    ensure(text_string in element.text, False, error_msg)


##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)
    time.sleep(1)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)
    time.sleep(1)