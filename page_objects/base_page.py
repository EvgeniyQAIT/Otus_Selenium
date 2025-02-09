from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def open(self, url):
        self.browser.get(url)

    def find_element(self, *locator):
        return self.browser.find_element(*locator)

    def find_elements(self, *locator):
        return self.browser.find_elements(*locator)

    def verify_title(self, expected_title):
        assert (
            expected_title in self.browser.title
        ), f"Текущий Title страницы {self.browser.title} отличается от ожидаемого: {expected_title}"

    def verify_title_with_wait(self, timeout, title):
        WebDriverWait(self.browser, timeout).until(EC.title_is(title))

    def check_element_present(self, *locator):
        self.find_element(*locator)

    def wait_find_element(self, *locator):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_find_elements(self, *locator):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_all_elements_located(locator)
        )
