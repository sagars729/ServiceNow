# ServiceNow

<p align="center">
  <img src="/pytest_terminal.png" alt="Terminal Output"/>
</p>

This repository details my project for the Division of Information Technology at the University of Maryland on automating Service Now testing using Selenium WebDriver.

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
echo -e "local_username\nlocal_password" > secret.txt
pytest
```

If you want more verbose output, consider adding the -s flag to pytest which enables all logs to print regardless of whether or not an error was encountered.
`pytest -s`

## Interpreting Results

If a test fails, there are usually two major reasons for this result:

1. The functionality of the application is flawed and a bug has been found
2. The functionality of the aplication has changed and the tests must be updated

**Usually**, if an AssertionError has caused the failure, a bug has been found; otherwise the tests must be updated. This **is not true in all cases** but can be used as a baseline for evaluating the results of pytest. 
