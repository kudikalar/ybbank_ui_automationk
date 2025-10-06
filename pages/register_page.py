from selenium.webdriver.common.by import By
from core.base_page import BasePage

class RegisterPage(BasePage):
    #Page Objects
    GENDER_MALE   = (By.ID, "gender-male")
    GENDER_FEMALE = (By.ID, "gender-female")
    FIRSTNAME     = (By.ID, "FirstName")
    LASTNAME      = (By.ID, "LastName")
    EMAIL         = (By.ID, "Email")
    PASSWORD      = (By.ID, "Password")
    CONFIRM_PWD   = (By.ID, "ConfirmPassword")
    REGISTER_BTN  = (By.ID, "register-button")
    RESULT_BANNER = (By.CSS_SELECTOR, "div.result")
    LOG_OUT_LINK = (By.LINK_TEXT,"Log out")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_register_page(self):
        self.open("/register")
        self.wait_url_contains("/register")
        self.wait_visible(self.REGISTER_BTN)

    def click_gender_male(self):         self.click(self.GENDER_MALE)
    def click_gender_female(self):       self.click(self.GENDER_FEMALE)
    def enter_first_name(self, v):       self.type(self.FIRSTNAME, v)
    def enter_last_name(self, v):        self.type(self.LASTNAME, v)
    def enter_email_address(self, v):    self.type(self.EMAIL, v)
    def enter_password(self, v):         self.type(self.PASSWORD, v)
    def enter_confirm_password(self, v): self.type(self.CONFIRM_PWD, v)
    def click_register_button(self):     self.click(self.REGISTER_BTN)
    def click_logout_link(self):
        self.click(self.LOG_OUT_LINK)

    def get_result_text(self):
        self.wait_visible(self.RESULT_BANNER)
        return self.text_of(self.RESULT_BANNER)
