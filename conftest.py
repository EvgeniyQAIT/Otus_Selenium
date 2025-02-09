import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--base_url", default="http://192.168.0.161:8081")
    parser.addoption("--headless", action="store_true")


@pytest.fixture()
def browser(pytestconfig):
    browser_name = pytestconfig.getoption("browser")
    base_url = pytestconfig.getoption("base_url")
    headless = pytestconfig.getoption("headless")

    driver = None

    if browser_name in ["ch", "chrome"]:
        options = ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser_name in ["ff", "firefox"]:
        options = FFOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)


    driver.maximize_window()
    driver.base_url = base_url

    yield driver

    driver.quit()