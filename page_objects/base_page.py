from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)
        self.logger = browser.logger
        self.class_name = type(self).__name__

    @allure.step("Открытие страницы")
    def open(self, url):
        self.logger.info("%s: Открытие страницы url: %s" % (self.class_name, url))
        self.browser.get(url)

    @allure.step("Поиск элемента")
    def find_element(self, *locator):
        self.logger.info("%s: Поиск элемента: %s" % (self.class_name, str(locator)))
        return self.browser.find_element(*locator)

    @allure.step("Поиск элементов")
    def find_elements(self, *locator):
        self.logger.info("%s: Поиск элементов: %s" % (self.class_name, str(locator)))
        return self.browser.find_elements(*locator)

    @allure.step("Проверка title страницы")
    def verify_title(self, expected_title):
        self.logger.info("%s: Проверка title страницы: %s" % (self.class_name, str(expected_title)))
        assert (
            expected_title in self.browser.title
        ), f"Текущий Title страницы {self.browser.title} отличается от ожидаемого: {expected_title}"

    @allure.step("Проверка title страницы через ожидание")
    def verify_title_with_wait(self, timeout, title):
        self.logger.info("%s: Проверка title страницы: ожидается %s" % (self.class_name, str(title)))
        WebDriverWait(self.browser, timeout).until(EC.title_is(title))

    @allure.step("Проверка элемента на странице")
    def check_element_present(self, *locator):
        self.logger.info("%s: Проверка элемента на  страницы: %s" % (self.class_name, str(locator)))
        self.find_element(*locator)

    @allure.step("Поиск элемента через ожидание")
    def wait_find_element(self, *locator):
        self.logger.info("%s: Поиск с ожиданием элемента: %s" % (self.class_name, str(locator)))
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Поиск элементов через ожидание")
    def wait_find_elements(self, *locator):
        self.logger.info("%s: Поиск с ожиданием элементов: %s" % (self.class_name, str(locator)))
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_all_elements_located(locator)
        )
