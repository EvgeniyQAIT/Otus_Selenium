from page_objects.admin_page import AdminPage
from page_objects.cart_page import CartPage
from page_objects.main_page import MainPage
from page_objects.catalog_page import VerifyPrice
import allure


@allure.title("Проверка входа под учеткой администратора и выход из учетки")
def test_login_logout_admin(browser):
    admin_page = AdminPage(browser)
    admin_page.go_to_administration()
    admin_page.verify_title("Administration")
    admin_page.login("user", "bitnami")
    admin_page.verify_title_with_wait(2, "Dashboard")
    admin_page.logout()
    admin_page.verify_title("Administration")


@allure.title("Проверка добавления товара в корзину, и проверка что они там есть")
def test_add_item_in_cart(browser):
    cart_item = CartPage(browser)
    cart_item.go_to_main_page()
    product_to_add = cart_item.add_item_to_cart(4)
    cart_item.verify_product_in_cart(product_to_add)


@allure.title("Проверка изменения отображения цены в валюте на главной странице")
def test_currency_change(browser):
    currency_main_page = MainPage(browser)
    currency_main_page.open()
    currency_main_page.check_current_prices()
    currency_main_page.change_currency_to_eur()
    currency_main_page.verify_currency_changed_to_eur()
    currency_main_page.change_currency_to_gbp()
    currency_main_page.verify_currency_changed_to_gbp()


@allure.title("Проверка изменения отображения цены в валюте на странице каталога товаров")
def test_page_catalog(browser):
    currency_catalog_page = VerifyPrice(browser)
    currency_catalog_page.go_to_catalog()
    currency_catalog_page.check_current_prices()
    currency_catalog_page.change_currency_to_eur()
    currency_catalog_page.verify_currency_changed_to_eur()
    currency_catalog_page.change_currency_to_gbp()
    currency_catalog_page.verify_currency_changed_to_gbp()