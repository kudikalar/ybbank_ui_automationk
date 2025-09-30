from selenium.webdriver.common.by import By
from core.base_page import BasePage
from utils.data_reader import read_excel

test_data = read_excel("data/register_test_data.xlsx")
class LoginPage(BasePage):
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    LOGIN_BTN = (By.XPATH, "/html/body/div[4]/div[1]/div[4]/div[2]/div/div[2]/div[1]/div[2]/div[2]/form/div[5]/input")
    LOGOUT_LINK =  (By.CLASS_NAME, "ico-logout")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_login_page(self):
        self.open("/login")
        self.wait_url_contains("/login")
        self.wait_visible(self.LOGIN_BTN)

    def enter_email(self, email):
        self.type(self.EMAIL, email)
    def enter_password(self, password):
        self.type(self.PASSWORD, password)
    def click_login(self):
        return self.click(self.LOGIN_BTN)
    def click_logout(self):
        return self.click(self.LOGOUT_LINK)












