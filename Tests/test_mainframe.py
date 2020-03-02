import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

import os
import pytest
import conftest
try:
    from mainframe import Mainframe
except:
    print("Module mainframe not found. Try running \"export PYTHONPATH=\".\"\" on the command line.")
    sys.exit(0)


chrome_driver_path = os.path.join(".", "chromedriver.exe")
headless = False

def init(headless = False):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-popup-blocking")

    if headless:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=options)
    mf = Mainframe(driver)
    mf.side_door_login()
    mf.impersonate("Jess Jacobson")
    return mf

def test_sanity():
    assert(1==1)

def test_c1_required_fields_1():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)
    mf.driver.quit()

def test_c1_required_fields_2():
    mf = init(headless)
    mf.navigate_to_form()
    mf.select_environment("Development")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket == None)    
    mf.driver.quit()

def test_c1_required_fields_4():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket == None)    
    mf.driver.quit()

def test_c1_required_fields_5():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    mf.select_application("ADM", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket == None)    
    mf.driver.quit()

def try_submit(mf):
    try:
        mf.submit_form(False)
        ticket, request = mf.check_submit()
        assert(ticket == None)
    except NoSuchElementException:
        print("Caught NoSuchElementException - Passed")

def test_c1_required_fields_6():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    
    mf.select_specific_dataset("", "read", "", "")
    try_submit(mf)

    mf.select_specific_dataset("", "read", "", "reason")
    try_submit(mf)

    mf.driver.quit()

def test_c2_2():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development") 
    mf.select_specific_dataset("ADM", "read", "*", "this is a reason to request")
 
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)    
    mf.driver.quit()

def test_c2_3():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development") 
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_specific_dataset("ADM", "read", "*", "this is a reason to request")
 
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)     
    mf.driver.quit()

def test_c2_4():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development") 
 
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket == None)    
    mf.driver.quit()

def test_c7_environment_help():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    assert(mf.get_environment_help() != None)
    
    mf.select_environment("Production")
    assert(mf.get_environment_help() != None)
    mf.driver.quit()

def test_c8_dataset_help():
    mf = init(headless)
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    assert(mf.get_dataset_help() != None)
    
    mf.select_environment("Production")
    assert(mf.get_dataset_help() != None)
    mf.driver.quit()
