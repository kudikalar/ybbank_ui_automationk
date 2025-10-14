from selenium.webdriver.common.by import By
from core.base_page import BasePage

class HomePage(BasePage):
    REGISTER_BTN = (By.CLASS_NAME, "btn register-btn")
    LOGIN_BTN    = (By.CLASS_NAME, "btn signin-btn")
    LOGO_IMAGE   = (By.CLASS_NAME, "logo")

    def __init__(self, driver, env):
        super().__init__(driver, env)  # env can be 'qa' or a full URL

    def open_home(self):
        self.open("/")
        self.wait_visible(self.LOGO_IMAGE)

    """Page object method"""
    def click_register_button(self):
        self.js_click(self.REGISTER_BTN)  # robust click

    def click_login_button(self):
        self.click(self.LOGIN_BTN)
