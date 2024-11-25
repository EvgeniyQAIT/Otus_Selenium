
def test_check_title(browser):
    browser.get("http://192.168.0.161:8081/")
    assert "Your Store" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_catalog(browser):
    browser.get("http://192.168.0.161:8081/en-gb/catalog/tablet")
    assert "Tablet" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_prodcut_card_iphone(browser):
    browser.get("http://192.168.0.161:8081/en-gb/product/iphone")
    assert "iPhone" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_registration_user(browser):
    browser.get("http://192.168.0.161:8081/en-gb?route=account/register")
    assert "Register Account" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_administration(browser):
    browser.get("http://192.168.0.161:8081/administration/")
    assert "Administration" in browser.title, "Тайтл страницы отличается от ожидаемого"


#