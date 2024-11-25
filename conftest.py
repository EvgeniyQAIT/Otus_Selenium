import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")


@pytest.fixture()
def browser(pytestconfig):
    browser_name = pytestconfig.getoption("browser")

    if browser_name in ["ch", "chrome"]:
        return webdriver.Chrome()
    elif browser_name in ["ff", "firefox"]:
        return webdriver.Firefox()