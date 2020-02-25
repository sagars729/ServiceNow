import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
from Mainframe import Mainframe

chrome_driver_path = os.path.join(".", "chromedriver.exe")
driver = webdriver.Chrome()#executable_path=chrome_driver_path)
    
mf = Mainframe(driver)
mf.login()


def test_required_fields():
    mf.impersonate("Jess Jacobson")
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    mf.submit_form(False)
    ticket, request = mf.check_submit()
    assert(ticket != None)
    
