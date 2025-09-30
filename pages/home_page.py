from selenium.webdriver.common.by import By
from core.base_page import BasePage

class HomePage(BasePage):
    REGISTER_LINK = (By.CSS_SELECTOR, "a.ico-register")
    LOGIN_LINK    = (By.CSS_SELECTOR, "a.ico-login")

    def __init__(self, driver, env):
        super().__init__(driver, env)  # env can be 'qa' or a full URL

    def open_home(self):
        self.open("/")

    """Page object method"""
    def click_register_link(self):
        self.click(self.REGISTER_LINK)  # robust click

    def click_login_link(self):
        self.click(self.LOGIN_LINK)
