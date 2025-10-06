from selenium.webdriver.common.by import By
from core.base_page import BasePage

class LoginPage(BasePage):
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.XPATH, "//*[@name='Password']")
    LOGIN_BTN = (By.XPATH, "//*[@value='Log in']")
    LOGIN_VERIFY = (By.XPATH, "//h2[contains(text(),'Welcome to our store')]")
    REMEMBER_ME_CHECK_BOX = (By.XPATH, "//*[@type='checkbox']")
    FORGOT_PWD_LINK = (By.XPATH, "//a[text()='Forgot password?']")
    LOGIN_ERROR = (By.XPATH, "//li[contains(text(),'No customer account found')]")
    LOGIN_ERROR_WITH_INVALID_EMAIL = (By.XPATH, "//span[contains(text(),'Please enter a valid email address.')]")
    LOGIN_ERROR_WITH_INVALID_PASSWORD = (By.XPATH, "//li[text()='The credentials provided are incorrect']")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_login_page(self):
        self.open("/login")
        self.wait_url_contains("/login")
        self.wait_visible(self.LOGIN_BTN)

    # One-line action methods
    def enter_email_address(self, email): self.type(self.EMAIL, email)
    def enter_password(self, pwd): self.type(self.PASSWORD, pwd)
    def click_login_btn(self): self.click(self.LOGIN_BTN)
    def click_remember_me_checkbox(self): self.click(self.REMEMBER_ME_CHECK_BOX)
    def click_forgot_pwd_link(self): self.click(self.FORGOT_PWD_LINK)

    # Verification / text methods
    def login_verify(self): return self.text_of(self.LOGIN_VERIFY)
    def login_with_empty_data_error(self): return self.text_of(self.LOGIN_ERROR)
    def login_with_invalid_emailID_error(self): return self.text_of(self.LOGIN_ERROR_WITH_INVALID_EMAIL)
    def login_with_invalid_password_error(self): return self.text_of(self.LOGIN_ERROR_WITH_INVALID_PASSWORD)