from page_objects.admin_page import AdminPage
from page_objects.cart_page import CartPage
from page_objects.main_page import MainPage
from page_objects.catalog_page import VerifyPrice
from page_objects.registr_user_page import RegistrationPage
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
    currency_main_page.open_main_page()
    currency_main_page.check_current_prices()
    currency_main_page.change_currency_to_eur()
    currency_main_page.verify_currency_changed_to_eur()
    currency_main_page.change_currency_to_gbp()
    currency_main_page.verify_currency_changed_to_gbp()


@allure.title("Проверка изменения отображения цены в валюте на странице каталога товаров")
def test_page_catalog(browser):
    currency_catalog_page = VerifyPrice(browser)
    currency_catalog_page.open_main_page()
    currency_catalog_page.check_current_prices()
    currency_catalog_page.change_currency_to_eur()
    currency_catalog_page.verify_currency_changed_to_eur()
    currency_catalog_page.change_currency_to_gbp()
    currency_catalog_page.verify_currency_changed_to_gbp()


@allure.title("Отображение всех нужных элементов на странице регистрации пользователя")
def test_page_register_users(browser):
    reg_user_page = RegistrationPage(browser)
    reg_user_page.open_reg_user_page()
    reg_user_page.verify_title("Register Account")
    reg_user_page.check_registration_user_form()

@allure.title("Аутентификация нового пользователя")
def test_auth(create_new_user, browser):
    user_data = create_new_user
    browser.get(browser.base_url)
    main = MainPage(browser)
    reg_page = RegistrationPage(browser)
    reg_page.login_user(user_data)
    main.logout_user()
    logout = reg_page.logout_assert()
    assert logout == "Account Logout"
    main.start_login_user()
    reg_page.login_user(user_data)
    assert reg_page.wait_find_element(RegistrationPage.LOGIN_ASSERT).text == "My Account"

@allure.title("Проверка работоспособности wish list")
def test_wish_list_not_register(browser):
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page._find_element(locator=RegistrationPage.WISH_LIST).click()
    assert (
        main_page._find_element(locator=RegistrationPage.NEW_CUSTOMER).text
        == "New Customer"
    )


@allure.title("Проверка перехода на страницу wish list")
def test_wish_list_with_register_user(browser, create_new_user):
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page._find_element(locator=RegistrationPage.WISH_LIST).click()
    main_page._find_element(locator=RegistrationPage.WISH_LIST_TOTAL)
    assert (
        main_page._find_element(locator=RegistrationPage.WISH_LIST_ACCOUNT).text
        == "My Wishlist"
    )

@allure.title("Проверка элементов на главной странице сервиса")
def test_main_page(browser):
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page.verify_title(main_page.TITLE)
    main_page.verify_quantity_cards(4)
    main_page.verify_quantity_banner(2)
    main_page.check_privacy_policy()

@allure.title("Проверка элементов на главной странице сервиса")
def test_main_page(browser):
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page.verify_title(main_page.TITLE)
    main_page.verify_quantity_cards(4)
    main_page.verify_quantity_banner(2)
    main_page.check_privacy_policy()
