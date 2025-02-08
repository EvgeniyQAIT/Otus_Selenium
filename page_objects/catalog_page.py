import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from page_objects.main_page import MainPage


class CatalogPage(BasePage):
    TITLE = "Tablets"
    TABLETS_LINK = (By.LINK_TEXT, "Tablets")
    PRODUCT_THUMB = (By.XPATH, "//*[@class='product-thumb']")
    COLUMN_LEFT = (By.ID, "column-left")
    BUTTON_LIST = (By.ID, "button-list")
    BUTTON_GRID = (By.ID, "button-grid")
    INPUT_SORT = (By.ID, "input-sort")

    @allure.step("Выполняется вход на страницу")
    def open(self, **kwargs):
        super().open(self.browser.base_url)

    @allure.step("Выбора категории 'Планшеты'")
    def select_tablets(self):
        self.find_element(*self.TABLETS_LINK).click()

    @allure.step("Проверка элементов на странице каталога")
    def check_elements(self):
        self.check_element_present(*self.PRODUCT_THUMB)
        self.check_element_present(*self.COLUMN_LEFT)
        self.check_element_present(*self.BUTTON_LIST)
        self.check_element_present(*self.BUTTON_GRID)
        self.check_element_present(*self.INPUT_SORT)

    @allure.step("Проверка наличия слова 'catalog' в адресной строке")
    def verify_catalog_url(self):
        assert (
            "catalog" in self.browser.current_url
        ), "URL страницы не содержит 'catalog'"


class VerifyPrice(CatalogPage, MainPage):
    SELECT_DESKTOPS = (
        By.XPATH,
        "//a[@data-bs-toggle='dropdown' and text()='Desktops']",
    )
    SHOW_ALL_DESKTOPS = (
        By.XPATH,
        "//*[@class='see-all' and text()='Show All Desktops']",
    )

    @allure.step("Выполнение перехода на страницу каталога")
    def go_to_catalog(self, **kwargs):
        MainPage.open(self)
        self.find_element(*self.SELECT_DESKTOPS).click()
        self.find_element(*self.SHOW_ALL_DESKTOPS).click()
        self.verify_catalog_url()
