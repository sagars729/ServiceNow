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
