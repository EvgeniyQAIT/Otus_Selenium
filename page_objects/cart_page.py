import time
from random import randint
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
import allure

class CartPage(BasePage):
    DESCRIPTION_PRODUCTS = (By.XPATH, "//*[@class='description']/h4/a")
    CART_ITEMS_BUTTON = (By.CSS_SELECTOR, 'button[formaction*="checkout/cart.add"]')
    SHOPPING_CART_LINK = (
        By.XPATH,
        "//*[contains(@class,'d-none') and text()='Shopping Cart']",
    )
    PRODUCT_NAME = (By.XPATH, "//td[contains(@class, 'text-wrap')]/a")

    @allure.step("Выполняется вход на главную страницу")
    def go_to_main_page(self):
        super().open(self.browser.base_url)

    @allure.step("Проверка добавления продукта в корзину")
    def add_item_to_cart(self, quantity_cards):
        products = self.find_elements(*self.DESCRIPTION_PRODUCTS)
        assert (
            len(products) == quantity_cards
        ), f"Количество найденных карточек {len(products)} не равно {quantity_cards}"
        item = randint(0, len(products) - 1)
        product_to_add = products[item].text
        cart_items = self.wait_find_elements(*self.CART_ITEMS_BUTTON)
        time.sleep(1)
        ActionChains(self.browser).move_to_element(cart_items[item]).perform()
        cart_items[item].click()
        return product_to_add

    @allure.step("Проверка добавленного продукта в корзине")
    def verify_product_in_cart(self, expected_product_name):
        cart = self.find_element(*self.SHOPPING_CART_LINK)
        ActionChains(self.browser).move_to_element(cart).perform()
        self.find_element(By.XPATH, "//button[@class='btn-close']").click()
        self.find_element(*self.SHOPPING_CART_LINK).click()
        product_name = self.find_element(*self.PRODUCT_NAME)
        assert product_name.text == expected_product_name, "Товар не найден в корзине"