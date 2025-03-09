from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
import allure
import time

class MainPage(BasePage):
    TITLE = "Your Store"
    ACCOUNT_LINK = (By.XPATH, "//*[contains(@class,'d-none') and text()='My Account']")
    CARD_ITEMS = (By.XPATH, "//*[@class='product-thumb']")
    BANNER_ITEMS = (By.XPATH, "//*[@data-bs-ride='carousel']")
    PRIVACY_POLICY_LINK = (By.LINK_TEXT, "Privacy Policy")
    CURRENCY_BUTTON = (By.XPATH, "//button[@data-bs-toggle='dropdown']")
    CURRENCY_LIST = (By.XPATH, "//*[contains(@class,'d-none') and text()='Currency']")
    EUR_OPTION = (By.XPATH, "//*[@href='EUR']")
    GBP_OPTION = (By.XPATH, "//*[@href='GBP']")
    PRICE_ELEMENTS = (By.XPATH, "//div[@class='price']")
    REGISTER = (By.XPATH, "//a[text()='Register']")
    LOGOUT = (By.XPATH, "//a[text()='Logout']")
    LOGIN = (By.XPATH, "//a[text()='Login']")
    SEARCH = (By.NAME, "search")
    LOUPE = (By.XPATH, "//*[@id='search']/button")
    ASSERT_SEARCH_PRODUCT = (By.XPATH, "//*[@id='content']")

    @allure.step("Открытие главной страницы")
    def open_main_page(self):
        super().open(self.browser.base_url)

    @allure.step("Переход в окно регистрации нового пользователя")
    def find_user(self):
        self.wait_find_element(self.ACCOUNT_LINK).click()
        self.wait_find_element(self.REGISTER).click()

    @allure.step("Пользователь разлогинивается")
    def logout_user(self):
        time.sleep(
            1.5
        )  # Страница дозагружается и сбрасывает раскрытое меню, приходится делать минислип, без него никак
        self._find_element(self.ACCOUNT_LINK).click()
        self._find_element(self.LOGOUT).click()

    @allure.step("Поиск продукта в строке поиска")
    def search_product(self, data):
        self.send_keys(element=self._find_element(self.SEARCH), text=data.name)
        self._find_element(self.LOUPE).click()

    @allure.step("Подтверждение найденного товара на странице")
    def assert_search_product(self):
        # time.sleep(0.5)  # Необходимо для того чтобы обновилась таблица на странице
        result = self._find_element(self.ASSERT_SEARCH_PRODUCT).text
        return result

    @allure.step("Логирование новым пользователем")
    def start_login_user(self):
        self.wait_find_element(self.ACCOUNT_LINK).click()
        time.sleep(0.5)
        self.wait_find_element(self.LOGIN).click()

    @allure.step("Проверка количества карточек на главной странице")
    def verify_quantity_cards(self, quantity_cards):
        card_items = self.find_elements(*self.CARD_ITEMS)
        assert (
            len(card_items) == quantity_cards
        ), f"Количество найденных карточек {len(card_items)} не равно {quantity_cards}]"

    @allure.step("Проверка количества баннеров на главной странице")
    def verify_quantity_banner(self, quantity_banner):
        banner_items = self.find_elements(*self.BANNER_ITEMS)
        assert (
            len(banner_items) == quantity_banner
        ), f"Количество найденных баннеров {len(banner_items)} не равно {quantity_banner}"

    @allure.step("Проверка политик безопасности на главной странице")
    def check_privacy_policy(self):
        self.check_element_present(*self.ACCOUNT_LINK)
        self.find_elements(*self.PRIVACY_POLICY_LINK)

    @allure.step("Проверка установленной текущей валюты на странице")
    def check_current_prices(self):
        price_button_cart = self.find_element(*self.CURRENCY_BUTTON)
        assert (
            "$" in price_button_cart.text
        ), "Цена на кнопке корзины не отображается со знаком $"

        for item in self.find_elements(*self.PRICE_ELEMENTS):
            price_element = item.find_element(By.XPATH, "//div[@class='price']/span")
            assert (
                "$" in price_element.text
            ), "Цена на карточке товара не отображается со знаком $"

    @allure.step("Изменение валюты на EUR на странице")
    def change_currency_to_eur(self):
        self.find_element(*self.CURRENCY_LIST).click()
        self.find_element(*self.EUR_OPTION).click()
        time.sleep(2)

    @allure.step("Проверка изменения валюты на EUR на странице")
    def verify_currency_changed_to_eur(self):
        price_button_cart = self.find_element(*self.CURRENCY_BUTTON)
        assert (
            "€" in price_button_cart.text
        ), "Цена на кнопке корзины не отображается со знаком €"

        for item in self.find_elements(*self.PRICE_ELEMENTS):
            price_element_currency = item.find_element(
                By.XPATH, "//div[@class='price']/span"
            )
            assert (
                "€" in price_element_currency.text
            ), "Цена на карточке товара не отображается со знаком €"

    @allure.step("Изменение валюты на GPB на странице")
    def change_currency_to_gbp(self):
        self.find_element(*self.CURRENCY_LIST).click()
        self.find_element(*self.GBP_OPTION).click()

    @allure.step("Проверка изменения валюты на GPB на странице")
    def verify_currency_changed_to_gbp(self):
        price_button_cart = self.find_element(*self.CURRENCY_BUTTON)
        assert (
            "£" in price_button_cart.text
        ), "Цена на кнопке корзины не отображается со знаком £"

        for item in self.find_elements(*self.PRICE_ELEMENTS):
            price_element_currency = item.find_element(
                By.XPATH, "//div[@class='price']/span"
            )
            assert (
                "£" in price_element_currency.text
            ), "Цена на карточке товара не отображается со знаком £"