from page_objects.main_page import MainPage
from page_objects.catalog_page import CatalogPage
from page_objects.product_card_page import ProductPage
from page_objects.admin_page import AdminPage
from page_objects.registr_user_page import RegistrPage
import allure


@allure.title("Проверка title на главной странице сервиса")
def test_main_page(browser):
    main_page = MainPage(browser)
    main_page.open()
    main_page.verify_title(main_page.TITLE)
    main_page.verify_quantity_cards(4)
    main_page.verify_quantity_banner(2)
    main_page.check_privacy_policy()


@allure.title("Проверка title на странице каталога")
def test_page_catalog(browser):
    catalog_page = CatalogPage(browser)
    catalog_page.open()
    catalog_page.select_tablets()
    catalog_page.verify_title(catalog_page.TITLE)
    catalog_page.verify_catalog_url()
    catalog_page.check_elements()


@allure.title("Проверка title на странице продукта")
def test_page_product(browser):
    product_page = ProductPage(browser)
    product_page.open_main_page()
    product_page.select_first_product()
    product_page.verify_title(product_page.TITLE)
    product_page.check_elements()


@allure.title("Проверка title на странице входа в администратора")
def test_admin_page(browser):
    admin_page = AdminPage(browser)
    admin_page.go_to_administration()
    admin_page.verify_title("Administration")
    admin_page.check_elements()


@allure.title("Проверка title на странице регистрации пользователя")
def test_page_register_users(browser):
    reg_user_page = RegistrPage(browser)
    reg_user_page.open()
    reg_user_page.verify_title("Register Account")
    reg_user_page.check_registration_user_form()
