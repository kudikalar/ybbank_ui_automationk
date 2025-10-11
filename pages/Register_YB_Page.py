from selenium.webdriver.common.by import By
from core.base_page import BasePage


class RegisterYBPage(BasePage):
    REGISTER_BTN = (By.XPATH, "//*[@id='navLinks']/a[5]")
    FULL_NAME_YB = (By.ID, "fullName")
    EMAIL_ID_YB = (By.ID, "email")
    PASSWORD_YB = (By.ID, "password")
    CONFIRM_PASSWORD = (By.ID, "confirm")
    REGISTER_SIGN_UP_BTN = (By.XPATH,"//*[@id='registerForm']/button")
    VERIFY_LOGIN_PAGE = (By.XPATH, "//*[text()='Banking App']")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_register_page(self):
        self.open("/#register")
        self.wait_url_contains("/#register")
        self.wait_visible(self.REGISTER_BTN)

    def enter_full_name_yb(self, full_name):
        self.type(self.FULL_NAME_YB, full_name)

    def enter_email_address(self, email):
        self.type(self.EMAIL_ID_YB, email)

    def enter_password(self, pwd):
        self.type(self.PASSWORD_YB, pwd)

    def enter_confirm_pwd(self, confirm_pwd):
        self.type(self.CONFIRM_PASSWORD, confirm_pwd)

    def click_register_sign_btn(self):
        self.click(self.REGISTER_SIGN_UP_BTN)

    def verify_login_yb(self):
        return self.text_of(self.VERIFY_LOGIN_PAGE)

    def get_page_title(self):
        return self.driver.title