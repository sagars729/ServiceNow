import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
from getpass import getpass

###This class is used to perform all actions on the agent view of ServiceNow
class ServiceNow():
    auth_page = "shib.idm.umd.edu"
    impl_wait = 30
    home_page = "https://umddev.service-now.com"

    def __init__(self, driver, logs=True):
        driver.implicitly_wait(self.impl_wait)
        self.driver = driver
        self.logs = logs
        if logs: 
            print("Created ServiceNow Object")
            print("Implicit Wait Time Set To", self.impl_wait)
        else: print("Logs Disabled")

    def log(self, s):
    	if self.logs: print(s)
    
    def login(self, directory_id=None, password=None):
    	self.log("Checking that user is logged in")
    	self.driver.get(self.home_page)
    	if self.auth_page not in self.driver.current_url: return
    
    	self.log("Requesting user credentials for login")
    	if not directory_id: directory_id = input("Directory ID: ")
    	if not password: password = getpass()
    
    	self.log("Logging in as " + directory_id)
    	self.driver.find_element(By.ID, "username").send_keys(directory_id)
    	self.driver.find_element(By.ID, "password").send_keys(password)
    	self.driver.find_element(By.CSS_SELECTOR, "body > div.wrapper > div > div.content > div.column.one > form > div:nth-child(4) > button").click()
    	
    	self.log("Sending Push To Duo")
    	self.driver.switch_to.frame(self.driver.find_element(By.ID, "duo_iframe"))
    	self.driver.find_element(By.CSS_SELECTOR, "#auth_methods > fieldset > div.row-label.push-label > button").click()
    	self.driver.switch_to.default_content()
    	WebDriverWait(self.driver, self.impl_wait*1000).until(expected_conditions.visibility_of_element_located((By.ID, "user_info_dropdown")))
    	
    	self.log("Logged in as " + directory_id)
    	return True
    
    def impersonate(self, user):
        self.log("Impersonating " + user)
        self.driver.get(self.home_page)

        #WebDriverWait(self.driver, 30000).until(expected_conditions.visibility_of_element_located((By.ID, "user_info_dropdown")))
        self.log("Finding " + user)
        self.driver.find_element(By.ID, "user_info_dropdown").click()
        self.driver.find_element(By.CSS_SELECTOR, "#glide_ui_impersonator").click()
        element = self.driver.find_element(By.ID, "select2-chosen-2")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.ID, "select2-drop-mask")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()

        WebDriverWait(self.driver, self.impl_wait*1000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#select2-results-2 > li")))
        self.driver.find_element(By.ID, "s2id_autogen2_search").send_keys(user)
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "#select2-results-2 > li").click() #send_keys(Keys.ENTER)
        self.log("Impersonated " + user)
        time.sleep(3)
        self.driver.get(self.home_page)

if __name__ == "__main__":
    chrome_driver_path = os.path.join(".","chromedriver.exe")
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    sn = ServiceNow(driver)
    sn.login()
    sn.impersonate("Jess Jacobson")
    input("Hit Enter To Close Page")
    driver.quit()
