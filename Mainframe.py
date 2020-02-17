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

if __name__ == '__main__':
    chrome_driver_path = os.path.join(".", "chromedriver.exe")
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    mf = Mainframe(driver)
    mf.login()
    mf.impersonate("Jess Jacobson")
    mf.navigate_to_form()
    mf.enter_manager("William Biddle")
    input("Hit Enter To Close Page")
    driver.quit()
