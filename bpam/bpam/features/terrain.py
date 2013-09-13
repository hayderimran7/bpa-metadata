import os
import random
import string

from lettuce import *

from selenium import webdriver
import lettuce_webdriver.webdriver

if "DISPLAY" not in os.environ:
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(800, 600))
else:
    display = None

@before.all
def set_browser():
    if display: display.start()
    world.browser = webdriver.Firefox()

@after.all
def clean_after_tests(result):
    world.browser.quit()
    if display: display.stop()
