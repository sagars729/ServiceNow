import pytest

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="Enable tests to Headless Selenium WebDriver")

@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--headless")
