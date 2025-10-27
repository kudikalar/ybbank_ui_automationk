from selenium.webdriver.common.by import By
from core.base_page import BasePage
import allure


class RegisterPage(BasePage):
    # Page Objects
    FIRSTNAME     = (By.ID, "first")
    LASTNAME      = (By.ID, "last")
    EMAIL         = (By.ID, "email")
    PASSWORD      = (By.ID, "pass")
    CONFIRM_PWD   = (By.ID, "confirm")
    REGISTER_BTN  = (By.ID, "submit")

    EMAIL_VALIDATION_ERROR           = (By.ID, "emailErr")
    ERROR_MESSAGE                    = (By.ID, "emailErr")
    CNF_PASSWORD_ERROR_MESSAGE       = (By.ID, "confirmErr")

    # From YW_T108_Registration_should_throw_error_message_when_password_field_is_empty
    PASSWORD_REQUIRED                = (By.ID, "passErr")
    CONFIRM_PASSWORD_REQUIRED        = (By.ID, "confirmErr")

    # From main branch
    FIRST_NAME_ERROR_MESSAGE         = (By.ID, "firstErr")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    @allure.step("Open Register Page")
    def open_register_page(self):
        self.open("/register.html")
        self.wait_url_contains("/register.html")
        self.wait_visible(self.REGISTER_BTN)

    @allure.step("Enter First Name: {v}")
    def enter_first_name(self, v):
        self.type(self.FIRSTNAME, v)

    @allure.step("Enter Last Name: {v}")
    def enter_last_name(self, v):
        self.type(self.LASTNAME, v)

    @allure.step("Enter Email Address: {v}")
    def enter_email_address(self, v):
        self.type(self.EMAIL, v)

    @allure.step("Enter Password")
    def enter_password(self, v):
        self.type(self.PASSWORD, v)

    @allure.step("Enter Confirm Password")
    def enter_confirm_password(self, v):
        self.type(self.CONFIRM_PWD, v)

    @allure.step("Click Register button")
    def click_register_button(self):
        self.click(self.REGISTER_BTN)

    def email_validation_error(self):
        return self.text_of(self.EMAIL_VALIDATION_ERROR)

    def get_email_error_text(self):
        return self.text_of(self.ERROR_MESSAGE).strip()

    def get_cnf_password_error_text(self):
        return self.text_of(self.CNF_PASSWORD_ERROR_MESSAGE).strip()

    def get_password_error_text(self):
        return self.text_of(self.PASSWORD_REQUIRED)

    def get_confirm_password_error_text(self):
        return self.text_of(self.CONFIRM_PASSWORD_REQUIRED)

    def get_first_name_error_text(self):
        return self.text_of(self.FIRST_NAME_ERROR_MESSAGE)
