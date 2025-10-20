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
    EMAIL_VALIDATION_ERROR = (By.ID,"emailErr")
    ERROR_MESSAGE = (By.ID, "emailErr")
    FIRSTNAME_ERROR_MSG = (By.ID, "firstErr")
    LASTNAME_ERROR_MSG = (By.ID, "lastErr")
    EMAIL_ADDRESS_ERROR_MSG = (By.XPATH,"//*[@id='emailErr']")
    PASSWORD_ERROR_MSG = (By.XPATH, "//*[@id='passErr']")
    CONFIRM_PWD_ERROR_MSG = (By.XPATH, "//*[@id='confirmErr']")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_register_page(self):
        self.open("/register.html")
        self.wait_url_contains("/register.html")
        self.wait_visible(self.REGISTER_BTN)

    def enter_first_name(self, v):       self.type(self.FIRSTNAME, v)
    def enter_last_name(self, v):        self.type(self.LASTNAME, v)
    def enter_email_address(self, v):    self.type(self.EMAIL, v)
    def enter_password(self, v):         self.type(self.PASSWORD, v)
    def enter_confirm_password(self, v): self.type(self.CONFIRM_PWD, v)
    def click_register_button(self):     self.click(self.REGISTER_BTN)
    def email_validation_error(self):    return self.text_of(self.EMAIL_VALIDATION_ERROR)
    def get_email_error_text(self):   return self.text_of(self.ERROR_MESSAGE).strip()
    def get_first_name_error_text(self): return self.text_of(self.FIRSTNAME_ERROR_MSG)
    def get_last_name_error_text(self): return self.text_of(self.LASTNAME_ERROR_MSG)
    def get_email1_error_text(self): return self.text_of(self.EMAIL_ADDRESS_ERROR_MSG)
    def get_password_error_text(self): return self.text_of(self.PASSWORD_ERROR_MSG)
    def get_confirm1_password_text(self): return self.text_of(self.CONFIRM_PWD_ERROR_MSG)
