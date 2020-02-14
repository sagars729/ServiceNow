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
        self.driver.get(self.form_url)


if __name__ == '__main__':
    chrome_driver_path = os.path.join(".", "chromedriver.exe")
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    mf = Mainframe(driver)
    mf.login()
    mf.impersonate("Jess Jacobson")
    mf.navigate_to_form()
    input("Hit Enter To Close Page")
    driver.quit()
