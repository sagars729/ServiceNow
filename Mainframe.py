import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import sys
import traceback
from service_now import ServiceNow

class Mainframe(ServiceNow):
    
    log_id = "Mainframe"
    form_url = 'https://umddev.service-now.com/itsupport?id=sc_cat_item&sys_id=9197ec3edbdc8410965bd5ab5e961963' 
    req_url = 'https://umddev.service-now.com/itsupport?id=my_requests'
    app_url = 'https://umddev.service-now.com/itsupport?id=approvals'
    temp_app_url = 'https://umddev.service-now.com/hosting?id=approvals'

    envs = {"development" : 2,
            "production" : 3,
            "both" : 4}
    accs = {"read" : 2,
            "update" : 3,
            "alter" : 4}
    apps = {"student": ["adm", "fin", "grd", "ies", "ori", "res", "sar", "sgc", "sis", "ssp"],
            "financial": ["pro", "rfe"],
            "business": ["cop", "edb", "mtr", "pay", "phr", "tvl"],
            "other": ["ann", "dcp", "din", "usm"]}
    expl_wait = 10

    def __init__(self, driver, logs=True):
        super().__init__(driver, logs)
    
    def log(self, s):
        if self.logs: print("%s:" % self.log_id, s)

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
        time.sleep(self.expl_wait)
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

    def select_specific_dataset(self, pre, access, ds, res=""):
        self.log("Selecting dataset %s.%s with access %s" % (pre, ds, access))
        self.driver.find_element(By.CSS_SELECTOR, ".m-r").click()
       
        self.log("Filling prefix %s" % pre)
        self.driver.find_element(By.CSS_SELECTOR, "#s2id_sp_formfield_dataset_prefix > a").click()
        self.driver.find_element(By.CSS_SELECTOR, "#select2-drop > div > input").send_keys(pre)
        time.sleep(self.expl_wait)
        self.driver.find_element(By.CSS_SELECTOR, "#select2-drop > div > input").send_keys(Keys.ENTER)
    
        self.log("Selecting access %s" % access)
        self.driver.find_element(By.CSS_SELECTOR, "#sp_formfield_dataset_access_type > label:nth-child(%d) > span" % self.accs[access.lower()]).click()
        
        self.log("Selecting dataset %s.%s" % (pre, ds))
        self.driver.find_element(By.ID, "sp_formfield_dataset_name").click()
        self.driver.find_element(By.ID, "sp_formfield_dataset_name").send_keys(ds)
        
        self.log("Filling reason for access")
        self.driver.find_element(By.ID, "sp_formfield_dataset_reason_for_access").click()
        self.driver.find_element(By.ID, "sp_formfield_dataset_reason_for_access").send_keys(res)
        
        self.driver.find_element(By.CSS_SELECTOR, "div.modal-footer.ng-scope > .btn-primary").click()

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
        if check: 
            ticket, request = self.check_submit()
            assert(ticket != None)
            return ticket, request

    def navigate_to_ticket(self, req, tic=None):
        super().navigate_to_ticket(req, "Mainframe", tic=tic)

    def get_chain(self, app, typ):
        user = self.user
        self.log("Finding Chain For " + typ + " Application " + app)
        mf.impersonate("Sagar Saxena")

        self.log("Navigating to Crosswalk Table")
        self.driver.find_element(By.ID, "filter").send_keys("Access Management Crosswalk")
        time.sleep(self.expl_wait)
        self.driver.find_element(By.CSS_SELECTOR, "#gsft_nav > div > magellan-favorites-list > ul > li.sn-widget.ng-scope.selected > div > div:nth-child(1) > a > div:nth-child(2) > span").click()
        time.sleep(self.expl_wait)

        self.log("Locating Row")
        self.driver.execute_script("document.getElementById(\"u_access_management_crosswalk_filter_toggle_image\").click()")
        self.driver.find_element(By.ID, "select2-chosen-2").click()
        self.driver.find_element(By.ID, "s2id_autogen2_search").send_keys("Approval For Access To")
        self.driver.find_element(By.ID, "s2id_autogen2_search").send_keys(Keys.ENTER)
         
    def verify_chain(self, app, typ, chain):
        return

if __name__ == '__main__':
    chrome_driver_path = os.path.join(".", "chromedriver.exe")
    driver = webdriver.Chrome()#executable_path=chrome_driver_path)

    try:
        mf = Mainframe(driver)
        mf.side_door_login()
        mf.impersonate("Jess Jacobson")
        mf.navigate_to_form()
        mf.enter_manager("Scott Gibson")
        mf.select_environment("Development")
        mf.select_application("ADM", "this is a reason to request access", typ="student")
        mf.select_application("FIN", typ="student")
        mf.select_specific_dataset("ADM", "Read", "test", "this is a reason to request access")
        ticket, request = mf.submit_form(True)
        mf.navigate_to_ticket(request, ticket)
        chain = mf.chain_approval(ticket, request)
        #mf.get_chain("ADM", "student")
    except:
        traceback.print_exc(file=sys.stdout)

    input("Hit Enter To Close Page")
    driver.quit()
