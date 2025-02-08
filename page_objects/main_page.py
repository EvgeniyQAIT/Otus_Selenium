from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
import allure

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

    @allure.step("Открытие главной страницы")
    def open(self, **kwargs):
        super().open(self.browser.base_url)

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