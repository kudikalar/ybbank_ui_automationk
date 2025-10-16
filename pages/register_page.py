from selenium.webdriver.common.by import By
from core.base_page import BasePage
import allure

class RegisterPage(BasePage):
    #Page Objects
    FIRSTNAME     = (By.ID, "first")
    LASTNAME      = (By.ID, "last")
    EMAIL         = (By.ID, "email")
    PASSWORD      = (By.ID, "pass")
    CONFIRM_PWD   = (By.ID, "confirm")
    REGISTER_BTN  = (By.ID, "submit")
    EMAIL_ALREADY_EXISTS = (By.ID, "emailErr")

    # Constructor
    def __init__(self, driver, env):
        super().__init__(driver, env)

    @allure.step("Open register page")
    def open_register_page(self):
        self.open("/register.html")
        self.wait_url_contains("/register.html")
        self.wait_visible(self.REGISTER_BTN)

    @allure.step("Enter first name: {1}")
    def enter_first_name(self, v):       self.type(self.FIRSTNAME, v)
    @allure.step("Enter last name: {1}")
    def enter_last_name(self, v):        self.type(self.LASTNAME, v)
    @allure.step("Enter email address: {1}")
    def enter_email_address(self, v):    self.type(self.EMAIL, v)
    @allure.step("Enter password: {1}")
    def enter_password(self, v):         self.type(self.PASSWORD, v)
    @allure.step("Enter confirm password: {1}")
    def enter_confirm_password(self, v): self.type(self.CONFIRM_PWD, v)
    @allure.step("Click register button")
    def click_register_button(self):     self.click(self.REGISTER_BTN)
    @allure.step("Get email already exists text")
    def get_email_already_exists_text(self):
        return self.text_of(self.EMAIL_ALREADY_EXISTS)
