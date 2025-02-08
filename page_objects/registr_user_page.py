from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
import allure

class RegistrPage(BasePage):
    TITLE = "Register Account"
    FIRSTNAME_INPUT = (By.ID, "input-firstname")
    LASTNAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    NEWSLETTER_INPUT = (By.XPATH, "//input[@id='input-newsletter']")
    AGREE_INPUT = (By.XPATH, "//input[@name='agree']")

    @allure.step("Открытие страницы регистрации пользователя")
    def open(self, **kwargs):
        super().open(f"{self.browser.base_url}/index.php?route=account/register")

    @allure.step("Проверка элементов на странице регистрации пользователя")
    def check_registration_user_form(self):
        self.find_element(*self.FIRSTNAME_INPUT)
        self.find_element(*self.LASTNAME_INPUT)
        self.find_element(*self.EMAIL_INPUT)
        self.find_element(*self.PASSWORD_INPUT)
        self.find_element(*self.SUBMIT_BUTTON)
        self.find_element(*self.NEWSLETTER_INPUT)
        self.find_element(*self.AGREE_INPUT)