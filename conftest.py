import json
import logging
import allure
import pytest
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from page_objects.registr_user_page import RegistrationPage



def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Browser for tests")
    parser.addoption(
        "--base_url",
        default="http://192.168.0.161:8081/",
        help="Base URL of the application",
    )
    parser.addoption(
        "--headless", action="store_true", help="Run browser in headless mode"
    )
    parser.addoption(
        "--log_level", action="store", default="WARNING", help="Set the logging level"
    )
    parser.addoption(
        "--executor",
        default=None,
        nargs="?",
        const="127.0.0.1",
        help="Executor address (default: 127.0.0.1 if not specified)",
    )
    parser.addoption(
        "--mobile", action="store_true", help="Run tests on mobile emulation"
    )
    parser.addoption("--vnc", action="store_true", help="Enable VNC server")
    parser.addoption("--logs", action="store_true", help="Enable logging of tests")
    parser.addoption("--video", action="store_true", help="Record video during tests")
    parser.addoption("--bv", help="Browser version")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != "passed":
        item.status = "failed"
    else:
        item.status = "passed"


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    base_url = request.config.getoption("--base_url")
    headless = request.config.getoption("--headless")
    log_level = request.config.getoption("--log_level")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")
    mobile = request.config.getoption("--mobile")

    # Если передан executor, но без конкретного адреса, то по умолчанию ставим "127.0.0.1"
    if executor is None:
        executor_url = None  # Локальный режим
    else:
        # Если executor передан, формируем URL для удаленного сервера
        executor_url = f"http://{executor}:4444/wd/hub"

    log_dir = os.path.join(os.path.dirname(__file__), "logs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger(request.node.name)
    log_path = os.path.join(log_dir, f"{request.node.name}.log")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info(
        "===> Test %s started at %s" % (request.node.name, datetime.datetime.now())
    )

    if browser_name in ["ch", "chrome"]:
        browser_name = "chrome"
        options = ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        if not executor:
            driver = webdriver.Chrome(options=options)
    elif browser_name in ["ff", "firefox"]:
        browser_name = "firefox"
        options = FFOptions()
        if headless:
            options.add_argument("--headless")
        if not executor:
            driver = webdriver.Firefox(options=options)
    elif browser_name in ["edge", "Edge", "MicrosoftEdge"]:
        browser_name = "MicrosoftEdge"
        options = EdgeOptions()
        if headless:
            options.add_argument("headless=new")
        if not executor:
            driver = webdriver.Edge(options=options)

    caps = {
        "browserName": browser_name,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": vnc,
            "name": request.node.name,
            "screenResolution": "1280x2000",
            "enableVideo": video,
            "enableLog": logs,
            "timeZone": "Europe/Moscow",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"],
        },
        "acceptInsecureCerts": True,
    }

    if executor:
        for k, v in caps.items():
            options.set_capability(k, v)

        driver = webdriver.Remote(command_executor=executor_url, options=options)

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities, indent=4, ensure_ascii=False),
        attachment_type=allure.attachment_type.JSON,
    )

    driver.log_level = log_level
    driver.logger = logger
    driver.test_name = request.node.name

    logger.info("Browser %s started" % browser)

    if not mobile:
        driver.maximize_window()

    driver.base_url = base_url

    def fin():
        driver.quit()
        logger.info(
            "===> Test %s finished at %s" % (request.node.name, datetime.datetime.now())
        )

    yield driver

    if request.node.status == "failed":
        allure.attach(
            name="failure_screenshot",
            body=driver.get_screenshot_as_png(),
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            name="page_source",
            body=driver.page_source,
            attachment_type=allure.attachment_type.HTML,
        )

    request.addfinalizer(fin)

@pytest.fixture
def create_new_user(browser):
    registration_page = RegistrationPage(browser)
    yield registration_page.create_new_user()

