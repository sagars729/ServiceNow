import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
from ServiceNow import ServiceNow

class Mainframe(ServiceNow):
    
    form_url = 'https://umddev.service-now.com/itsupport?id=sc_cat_item&sys_id=9197ec3edbdc8410965bd5ab5e961963' 
    envs = {"development" : 2,
            "production" : 3,
            "both" : 4}
    apps = {"student": ["adm", "fin", "grd", "ies", "ori", "res", "sar", "sgc", "sis", "ssp"],
            "financial": ["pro", "rfe"],
            "business": ["cop", "edb", "mtr", "pay", "phr", "tvl"],
            "other": ["ann", "dcp", "din", "usm"]}

    def __init__(self, driver, logs=True):
        super().__init__(driver, logs)
    
    def navigate_to_form(self):
        self.log("Navigating to Access Management Mainframe Form")
        self.driver.get(self.form_url)

    def enter_manager(self, manager):
        field = "select2-drop-mask"
        inp = "#select2-drop > div > input"
        res = "#select2-results-6 > li"

        self.log("Locating Field")
        element = self.driver.find_element(By.LINK_TEXT, "Lookup using list")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.ID, field)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        
        self.log("Selecting Manager " + manager)
        self.driver.find_element(By.CSS_SELECTOR, inp).send_keys(manager)
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, res).click()
        self.log("Selected Manager " + manager)

    def select_environment(self, env):
        self.log("Selecting Environment " + env + " ID: %d" % self.envs[env.lower()])
        self.driver.find_element(By.CSS_SELECTOR, "#sp_formfield_environments > label:nth-child(%d) > span" % self.envs[env.lower()]).click()

    def select_application(self, app, res="", typ="student"):
        self.log("Selecting " + typ.capitalize() + " Application: " + app)
        self.driver.find_element(By.ID, "sp_formfield_access_" + app.lower()).click()
        
        self.log("Filling Reason: " + res) 
        self.driver.find_element(By.ID, "sp_formfield_reason_of_request_" + typ.lower()).click()
        self.driver.find_element(By.ID, "sp_formfield_reason_of_request_" + typ.lower()).send_keys(res)

    def select_specific_dataset():
        pass

    def submit_form(self, check=False):
        self.log("Submitting Form")
        actions = ActionChains(self.driver)
        btn = self.driver.find_element(By.NAME, "submit")

        self.log("Clicking Submit")
        self.driver.execute_script("$(\".btn-block\").click()")
        
        self.log("Agreeing to Statement of Understanding")
        self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled").click()
        time.sleep(3)
        if check: self.assert_submit()

    def assert_submit(self):
        self.log("Checking That Form Was Submitted")
        elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "RITM")
        assert(len(elements) > 0)
        ticket = self.driver.find_element(By.PARTIAL_LINK_TEXT, "RITM").text
        self.log("Ticket: " + ticket)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "RITM").click()

    
if __name__ == '__main__':
    chrome_driver_path = os.path.join(".", "chromedriver.exe")
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    
    mf = Mainframe(driver)
    mf.login()
    mf.impersonate("Jess Jacobson")
    mf.navigate_to_form()
    mf.enter_manager("William Biddle")
    mf.select_environment("Development")
    mf.select_application("ADM", "this is a reason to request access")
    mf.submit_form(True)

    input("Hit Enter To Close Page")
    driver.quit()
