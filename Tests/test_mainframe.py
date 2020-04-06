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
#import conftest
import sys
try:
    from mainframe import Mainframe
except:
    print("mainframe module not found\nTrying new path: .")
    sys.path.insert(0, os.path.abspath("."))
    from mainframe import Mainframe


chrome_driver_path = os.path.join(".", "chromedriver.exe")
try: headless = os.environ["HEADLESS"].lower() == 'true' 
except: headless = False

def init():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-popup-blocking")

    if headless:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=options)
    mf = Mainframe(driver)
    mf.side_door_login()
    mf.impersonate("Sagar Saxena")
    return mf

def cleanup_ticket(mf, approver, ticket, request):
    mf.approve_ticket(approver, ticket, request, reject=True)

@pytest.mark.sanity
def test_sanity():
    assert(1==1)

def test_c1_required_fields_1():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)
    cleanup_ticket(mf, "Scott Gibson", ticket, request)

    mf.driver.quit()

def test_c1_required_fields_2():
    mf = init()
    mf.navigate_to_form()
    mf.select_environment("Development")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket == None)    
    mf.driver.quit()

def test_c1_required_fields_4():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket == None)    
    mf.driver.quit()

def test_c1_required_fields_5():
    mf = init()
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
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    
    mf.select_specific_dataset("", "read", "", "")
    try_submit(mf)
    
    mf.driver.quit()

def test_c1_required_fields_6_2():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    
    mf.select_specific_dataset("thisIsNotAValidDataset1234", "read", "", "reason")
    try_submit(mf)

    mf.driver.quit()

def test_c2_2_application():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development") 
    mf.select_specific_dataset("ADM", "read", "*", "this is a reason to request")
 
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)    
    
    cleanup_ticket(mf, "Scott Gibson", ticket, request)
    mf.driver.quit()

def test_c2_3_application_and_dataset():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development") 
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_specific_dataset("ADM", "read", "*", "this is a reason to request")
 
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)     
    
    cleanup_ticket(mf, "Scott Gibson", ticket, request)
    mf.driver.quit()

def test_c2_4_no_application_or_dataset():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development") 
 
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket == None)    
    mf.driver.quit()

def test_c7_environment_help():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    assert(mf.get_environment_help() != None)
    
    mf.select_environment("Production")
    assert(mf.get_environment_help() != None)
    mf.driver.quit()

def test_c8_dataset_help():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    assert(mf.get_dataset_help() != None)
    
    mf.select_environment("Production")
    assert(mf.get_dataset_help() != None)
    mf.driver.quit()

def help_m1_approval_chain(env="Development", apps={"student":["ADM", "FIN"], "financial":["PRO", "RFE"]}, res={"student":"this is a reason to request access", "financial": "this is a reason to request access"}):
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment(env)
    for typ in apps:
        for app in apps[typ]:
            mf.select_application(app, res[typ], typ=typ)
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)
    
    chain = mf.chain_approval(ticket, request)
    mf.driver.quit()
    return chain

def test_m1_approval_manager():
    chain = help_m1_approval_chain()
    st = set(chain)
    assert("Scott Gibson" in st)


def test_m1_approval_no_duplicate():
    chain = help_m1_approval_chain()
    st = set(chain)
    assert(len(st) == len(chain) or len(chain) == 5)

def test_m1_approval_adm():
    chain = help_m1_approval_chain()
    st = set(chain)
    assert("Jing Jeng" in st)


def test_m1_approval_fin():
    chain = help_m1_approval_chain()
    st = set(chain)
    assert("Elwyn Fleming" in st)

def test_m1_approval_pro():
    chain = help_m1_approval_chain()
    st = set(chain)
    assert("Carrie Bredenkamp" in st)

def test_m1_approval_rfe():
    chain = help_m1_approval_chain()
    st = set(chain)
    assert("Carrie Bredenkamp" in st)

def test_m1_approval_prd_adm():
    chain = help_m1_approval_chain(env="Production", apps={"student":["ADM"]}, res={"student":"this is a reason to request access"})
    st = set(chain)
    assert("Jesse Galve" in st)

def test_m1_approval_prd_fin():
    chain = help_m1_approval_chain(env="Production", apps={"student":["FIN"]}, res={"student":"this is a reason to request access"})
    st = set(chain)
    assert("Jesse Galve" in st or "Kim Viapiano" in st)

@pytest.mark.debug
def test_m2_reject_man():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Production")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)
    
    chain = mf.chain_approval(ticket, request, [False])
    st = set(chain)
    assert("Jing Jeng" not in st)

    mf.driver.quit()

@pytest.mark.debug
def test_m2_reject_step_one():
    mf = init()
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Production")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)
    
    chain = mf.chain_approval(ticket, request, [True, False])
    st = set(chain)
    assert("Jesse Galve" not in st)

    mf.driver.quit()

def test_m4_approver_req():
    mf = init()
    mf.impersonate("Carrie Bredenkamp")
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    mf.select_application("PRO", "this is a reason to request access", typ="financial")
    mf.select_application("RFE", typ="financial")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)
    
    chain = mf.chain_approval(ticket, request)
    st = set(chain)
    assert("Carrie Bredenkamp" in st)

    mf.driver.quit()


#def test_m1_approval_prd_rfe():
#    chain = help_m1_approval_chain(env="Production")
#    st = set(chain)
#    assert("Dave Rieger" in st)
#
#def test_m1_approval_prd_pro():
#    chain = help_m1_approval_chain(env="Production")
#    st = set(chain)
#    assert("Marty Newman" in st or "Chenise Patterson")
