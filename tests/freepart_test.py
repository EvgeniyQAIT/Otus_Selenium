from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


url_param = "http://192.168.0.161:8081"

def test_login(browser):
    browser.get(f"{url_param}/en-gb?route=account/login")
    browser.find_element(By.ID, "input-email").send_keys("Evgeniy.qait@gmail.com")
    browser.find_element(By.ID, "input-password").send_keys("qwerty123")
    browser.find_element(By.XPATH, '//*[@id="form-login"]/div[3]/button').click()
    WebDriverWait(browser, timeout=2).\
        until(EC.url_contains("customer_token"))
    assert "My Account" in browser.title


def test_add_card(browser):
    browser.get(f"{url_param}/en-gb?route=common/home")
    button1 = browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div[2]/form/div/button[1]')
    actions = ActionChains(browser)
    actions.move_to_element(button1).perform()
    button1.click()
    WebDriverWait(browser, timeout=8).\
        until(EC.visibility_of_element_located((By.XPATH, '//*[@id="alert"]/div')))
    WebDriverWait(browser, timeout=3).\
        until(EC.visibility_of_element_located((By.XPATH, '//*[@id="alert"]/div/button'))).click()
    browser.find_element(By.XPATH, '//*[@id="header-cart"]/div/button').click()
    assert 'iPhone' in browser.find_element(By.XPATH, '//*[@id="header-cart"]/div/ul/li/table/tbody/tr/td[2]/a').text


def test_currency_home(browser):
    browser.get(f"{url_param}/en-gb?route=common/home")
    browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/a/span').click()
    browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/ul/li[1]/a').click()
    assert '€' in browser.find_element(By.CLASS_NAME, 'price-new').text


def test_currency_tablets(browser):
    browser.get(f"{url_param}/en-gb/catalog/tablet")
    browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/a/span').click()
    browser.find_element(By.XPATH, '//*[@id="form-currency"]/div/ul/li[1]/a').click()
    assert '€' in browser.find_element(By.CLASS_NAME, 'price-new').text

