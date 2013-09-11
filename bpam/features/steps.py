import os
import random
import string

from lettuce import *

from selenium import webdriver
import lettuce_webdriver.webdriver

from lettuce_webdriver.webdriver import contains_content

@step('I fill in "(.*)" with "(.*)" year')
def fill_in_year_type(step, field, value):
    year_field = world.browser.find_element_by_xpath('.//input[@id="%s"][@type="year"]' % field)
    year_field.clear()
    year_field.send_keys(value)

@step('I fill in "(.*)" with random text')
def fill_in_year_type(step, field):
    field = find_field_only(field)
    value = generate_random_str(8)
    field.clear()
    field.send_keys(value)

@step('I log in as "(.*)" with "(.*)" password expects "(.*)"')
def login_as_user(step, username, password, expectation):
    username_field = world.browser.find_element_by_xpath('.//input[@name="username"]')
    username_field.send_keys(username)
    password_field = world.browser.find_element_by_xpath('.//input[@name="password"]')
    password_field.send_keys(password)
    password_field.submit()
    assert contains_content(world.browser, expectation)

def generate_random_str(length):
    s = string.lowercase + string.uppercase
    return ''.join(random.sample(s,length))

def find_field_only(field):
    return find_field_no_value_by_id(field) or \
            find_field_no_value_by_name(field)
    
def find_field_no_value_by_id(field):
    ele = world.browser.find_elements_by_xpath('.//input[@id="%s"]' % field)
    if not ele:
        return False
    return ele[0]

def find_field_no_value_by_name(field):
    ele = world.browser.find_elements_by_xpath('.//input[@name="%s"]' % field)
    if not ele:
        return False
    return ele[0]