from lettuce import *

from lxml import html
from django.test.client import Client
from nose.tools import assert_equals

@before.all
def set_browser():
    world.browser = Client()

@step(u'Given I open "(.*)"')
def access_url(step, url):
    response = world.browser.get(url)
    world.dom = html.fromstring(response.content)

@step(u'Then I should see the heading "(.*)"')
def see_header(step, text):
    header = world.dom.cssselect('h1')[0]
    assert header.text == text, header.text

@step(u'When I fill in "(.*)" with "(.*)" and submit to url "(.*)"')
def when_i_fill_in_field_with_value(step, field, value, url):
    world.response = world.browser.post(url, {field: value})

@step(u'Then I should see "(.*)"')
def then_i_should_see_text(step, text):
    assert text in world.response.content, world.response
    
@step(u'And I should see "(.*)" within "(.*)"')
def and_i_should_see_text_within_selector(step, text, selector):
    world.dom = html.fromstring(world.response.content)
    assert text in world.dom.cssselect(selector)[0].text, world.dom.cssselect(selector)[0]

@step(u'When I fill in "(.*)" with "(.*)" and submit the form to url "(.*)"')
def when_i_fill_in_field_with_value_and_submit_the_form(step, field, value, url):
    world.response = world.browser.get(url, {field : value})