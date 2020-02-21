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
    req_url = 'https://umddev.service-now.com/itsupport?id=my_requests'
    app_url = 'https://umddev.service-now.com/itsupport?id=approvals'

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

    #EXPLICIT WAIT SHOULD BE REPLACED
    def enter_manager(self, manager):
        field = "select2-drop-mask"
        inp = "#select2-drop > div > input"
        res = "#select2-results-6 > li"

        self.log("Including all managers")
        time.sleep(self.expl_wait)
        self.driver.execute_script("$(\"#sp_formfield_show_all_manager\").click()")

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
        #self.driver.find_element(By.ID, "sp_formfield_access_" + app.lower()).click()
        self.driver.execute_script("$(\"#sp_formfield_access_%s\").click()" % app.lower())

        self.log("Filling Reason: " + res) 
        self.driver.find_element(By.ID, "sp_formfield_reason_of_request_" + typ.lower()).click()
        self.driver.find_element(By.ID, "sp_formfield_reason_of_request_" + typ.lower()).send_keys(res)

    def select_specific_dataset():
        pass

    #This method should be added to either the ServiceNow Class or a Super Class For Forms To Avoid Duplication
    #EXPLICIT WAIT SHOULD BE REPLACED
    def submit_form(self, check=False):
        self.log("Submitting Form")
        actions = ActionChains(self.driver)
        btn = self.driver.find_element(By.NAME, "submit")

        self.log("Clicking Submit")
        self.driver.execute_script("$(\".btn-block\").click()")
        
        self.log("Agreeing to Statement of Understanding")
        sou = "body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled"
        self.driver.execute_script("$(\"" + sou + "\").click()")

        time.sleep(self.expl_wait)
        if check: return self.assert_submit()

    #This method should be added to either the ServiceNow Class or a Super Class For Forms To Avoid Duplication
    def assert_submit(self):
        self.log("Checking That Form Was Submitted")
        elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "RITM")
        assert(len(elements) > 0)

        ticket = self.driver.find_element(By.PARTIAL_LINK_TEXT, "RITM").text
        self.log("Ticket: " + ticket)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "RITM").click()
        
        fields = self.driver.find_elements(By.CLASS_NAME, "select2-chosen")
        for f in fields:
            if "REQ" in f.text: 
                self.log("Request: " + f.text)
                return ticket, f.text
        
        return ticket, None

    #This method should be added to either the ServiceNow Class or a Super Class For Forms To Avoid Duplication
    def navigate_to_ticket(self, req, tic=None):
        self.log("Navigating To Ticket With Request: " + req)
        self.driver.get(self.req_url)
        elements = self.driver.find_elements(By.CLASS_NAME, "main-column")
        for e in elements:
            if req in e.text: 
                self.log("Found Request " + req)
                e.find_element(By.PARTIAL_LINK_TEXT, "Mainframe").click()
                
                ritm = self.driver.find_element(By.PARTIAL_LINK_TEXT, "RITM")
                if ritm.text == tic: self.log("Ticket Verified " + ritm.text)
                ritm.click()

                return True
        return False

    #This method should be added to either the ServiceNow Class or a Super Class For Forms To Avoid Duplication
    def get_approvers(self):
        self.log("Finding Approvers")
        els = self.driver.find_elements(By.CLASS_NAME, "col-xs-6")
        alt = self.driver.find_elements(By.CSS_SELECTOR, ".col-xs-1 > span")
        app = []
        for i, e in enumerate(els): 
            app.append((e.text.split("\n")[0], alt[i].get_attribute("alt")))
        for a in app: 
            self.log("Found Approver %s with status %s" % a)
        return app

    #This method should be added to either the ServiceNow Class or a Super Class For Forms To Avoid Duplication
    def approve_ticket(self, approver, ticket, request, user=None):
        mf.impersonate(approver)
        self.driver.get(self.app_url)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, ticket).click()
        self.driver.find_element(By.NAME, "approve").click()
        if user != None: mf.impersonate(user)

	
if __name__ == '__main__':
    chrome_driver_path = os.path.join(".", "chromedriver.exe")
    driver = webdriver.Chrome()#executable_path=chrome_driver_path)
    
    mf = Mainframe(driver)
    mf.login()
    mf.impersonate("Jess Jacobson")
    mf.navigate_to_form()
    mf.enter_manager("Scott Gibson")
    mf.select_environment("Development")
    mf.select_application("ADM", "this is a reason to request access", typ="student")
    mf.select_application("FIN", typ="student")
    ticket, request = mf.submit_form(True)
    mf.navigate_to_ticket(request, ticket)
    apps = mf.get_approvers() 
    for a in apps:
        mf.approve_ticket(a[0], ticket, request, "Jess Jacobson")
    input("Hit Enter To Close Page")
    driver.quit()
