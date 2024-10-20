
def test_check_title(browser): #тест на проверку заголовка главной страницы
    browser.get("http://192.168.0.161:8081/")
    assert "Your Store" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_catalog(browser): #тест на проверку заголовка карточек товара
    browser.get("http://192.168.0.161:8081/en-gb/catalog/tablet")
    assert "Tablet" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_prodcut_card_iphone(browser): #тест на проверку заголовка карточки айфона
    browser.get("http://192.168.0.161:8081/en-gb/product/iphone")
    assert "iPhone" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_registration_user(browser): #тест на проверку заголовка регистрации пользователя
    browser.get("http://192.168.0.161:8081/en-gb?route=account/register")
    assert "Register Account" in browser.title, "Тайтл страницы отличается от ожидаемого"

def test_check_title_administration(browser): #тест на проверку заголовка страницы администатора
    browser.get("http://192.168.0.161:8081/administration/")
    assert "Administration" in browser.title, "Тайтл страницы отличается от ожидаемого"

#ferwfew