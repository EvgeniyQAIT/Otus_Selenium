from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_login(browser):
    browser.get("http://192.168.0.161:8081/en-gb?route=account/login")
    browser.find_element(By.ID, "input-email").send_keys("Evgeniy.qait@gmail.com") #нашли элемент логин и ввели логин
    browser.find_element(By.ID, "input-password").send_keys("qwerty123") #нашли элемент пароль и ввели пароль
    browser.find_element(By.XPATH, '//*[@id="form-login"]/div[3]/button').click() #нашли кнопку и нажали
    WebDriverWait(browser, timeout=2).until(EC.url_contains("customer_token")) #подождали пока URL поменяется и там в URL будет токен
    assert "My Account" in browser.title #проверили заголовок страницы

def test_add_card(browser):
    browser.get("http://192.168.0.161:8081/en-gb?route=common/home")
    browser.maximize_window() #сделали максимальный размер окна
    button = browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div[2]/form/div/button[1]') #нашли кнопку добавления в корзину
    actions = ActionChains(browser)
    actions.move_to_element(button).perform() #пролистали до кнопки
    button.click() #добавили в корзину кликнув
    button2 = browser.find_element(By.XPATH, '//*[@id="header-cart"]/div/button') #нашли кнопку корзины
    actions = ActionChains(browser)
    actions.move_to_element(button2).perform() #пролистали до кнопки
    button2.click() #кликнули в корзину
# при выполнение теста test_add_card вылезает ошибка и я не пойму как её победить, он не видит элемент


def test_currency_home(browser):
    browser.get("http://192.168.0.161:8081/en-gb?route=common/home")
    button1 = browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/a/span') #нашли элемент переключения валюты
    button1.click() #кликнули
    button2 = browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/ul/li[1]/a') #нашли элемент евро
    button2.click() #переключили валюту кликнув на элемент
#надо как-то проверить что текст с $ сменился на € на главной странице у цены товаров



# def test_currency_tablets(browser):
#     browser.get("http://192.168.0.161:8081/en-gb/catalog/tablet")
#     button1 = browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/a/span')
#     button1.click()
#     button2 = browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/ul/li[1]/a')
#     button2.click()
#
# fwer