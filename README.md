# ServiceNow Test Automation

<p align="center">
  <img src="/pytest_terminal.png" alt="Terminal Output"/>
</p>

This repository details my project for the Division of Information Technology at the University of Maryland on automating Service Now testing using Selenium WebDriver. 

This is the latest version of this project, but it is also available on Bitbucket. If you have the correct authorization, you can access this project [here](https://bitbucket.umd.edu/projects/SOFTWAREDEVELOPMENTSUPPORT/repos/servicenowautomation/browse).

1. [Running This Project](#Running-This-Project)
2. [Interpreting Results](#Interpreting-Results)
3. [Writing Custom Tests](#Writing-Custom-Tests)

## Prerequisites

1. Install [Chrome](https://www.google.com/chrome/)
2. Install [ChromeDriver](https://chromedriver.chromium.org/getting-started)
3. Install [Python3](https://www.python.org/downloads/)
4. Install the required packages 
```python
pip install -r requirements.txt
```

## Running This Project

If you are an employee at DIT or if you have the correct credentials to run this project, follow the steps below:

1. Clone this repository git@github.com:sagars729/ServiceNow.git
2. Navigate to this repository and add the repository to the Python Path
3. Create a file called "secret.txt" in this repository. Put the username of a local ServiceNow user on the first line and the password of that user on the second line.
4. Run pytest

```bash
git clone git@github.com:sagars729/ServiceNow.git
cd /YourPathTo/ServiceNow
export PYTHONPATH="."
export HEADLESS=false
echo -e "local_username\nlocal_password" > secret.txt
pytest
```

If you want more verbose output, consider adding the -s flag to pytest which enables all logs to print regardless of whether or not an error was encountered.

`pytest -s`

If you want to run the tests without opening the Chrome browser (i.e. headless mode), run this command before you run pytest:

`export HEADLESS=true`

## Interpreting Results

If a test fails, there are usually two major reasons for this result:

1. The functionality of the application is flawed and a bug has been found
2. The functionality of the aplication has changed and the tests must be updated

**Usually**, if an AssertionError has caused the failure, a bug has been found; otherwise the tests must be updated. This **is not true in all cases** but can be used as a baseline for evaluating the results of pytest. 

## Writing Custom Tests

To write a custom pytest, perform the following steps:

1. Create a file named test_(your_test_file).py in the Tests folder.
2. Import the following packages in your python file

```python
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
```

3. Use the following code to create a ServiceNow object

```python
headless = False

options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")

if headless:
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    
driver = webdriver.Chrome(options=options)
sn = ServiceNow(driver)
```

4. Log in to ServiceNow Using the Side Door or CASS
```python
# Side Door Login
sn.side_door_login()

#CASS Login
sn.login()
```

5. Write a function for your custom test
```python
def test_your_test_name():
  # Write your test here
```

6. Run your test by navigating to the ServiceNow directory and running pytest
```bash
export PYTHONPATH="."
pytest Tests/test_your_test_file.py
```
