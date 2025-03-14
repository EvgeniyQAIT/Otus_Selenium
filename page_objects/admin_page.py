from selenium.webdriver.common.by import By


from page_objects.base_page import BasePage
import allure

class AdminPage(BasePage):
    USERNAME_INPUT = (By.ID, "input-username")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGOUT_LINK = (By.XPATH, "//*[contains(text(), 'Logout')]")
    LOGIN_MESSAGE = (
        By.XPATH,
        "//*[@class='card-header' and text()=' Please enter your login details.']",
    )
    DASHBOARD_TITLE = "Dashboard"

    @allure.step("Выполняется вход на страницу")
    def go_to_administration(self):
        self.browser.get(f"{self.browser.base_url}/administration")

    @allure.step("Выполняется проверка элементов на странице admin")
    def check_elements(self):
        self.check_element_present(*self.USERNAME_INPUT)
        self.check_element_present(*self.PASSWORD_INPUT)
        self.check_element_present(*self.SUBMIT_BUTTON)
        self.check_element_present(*self.LOGIN_MESSAGE)

    @allure.step("Выполняется ввод username и password")
    def login(self, username, password):
        self.browser.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.browser.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.browser.find_element(*self.SUBMIT_BUTTON).click()

    @allure.step("Выполняется выход из учетной записи admin")
    def logout(self):
        self.browser.find_element(*self.LOGOUT_LINK).click()