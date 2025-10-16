# pages/login_page.py
import allure
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from core.base_page import BasePage

class LoginPage(BasePage):
    # --- Locators aligned to your UI ---
    WELCOME_TITLE = (By.XPATH, "//h1[normalize-space()='Welcome Back']")
    ERROR_BANNER = (By.XPATH, "//*[contains(text(),'Please fix the errors above')]")

    EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='you@example.com']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Enter password']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Login']")
    REMEMBER_ME = (By.XPATH, "//label[contains(.,'Remember')]/preceding-sibling::input | //input[@type='checkbox']")

    EMAIL_REQUIRED_ERROR = (By.XPATH, "//*[text()='Email is required.']")
    PASSWORD_REQUIRED_ERROR = (By.XPATH, "//*[text()='Password is required.']")
    LOGIN_INVALID_CRED_ERROR = (By.XPATH, "//*[contains(text(),'incorrect') or contains(text(),'Invalid')]")
    LOGIN_INVALID_EMAIL_ERROR = (By.XPATH, "//div[contains(text(),'Invalid email format.')]")

    LOGIN_SUCCESS_BANNER = (By.XPATH, "//*[contains(text(),'Welcome to our store') or contains(@class,'welcome')]")

    REGISTER_LINK = (By.LINK_TEXT, "Register here")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")

    # --- Backward-compat aliases (so existing tests still work) ---
    LOGIN_VERIFY = LOGIN_SUCCESS_BANNER
    LOGIN_ERROR = ERROR_BANNER
    LOGIN_ERROR_WITH_INVALID_EMAIL = EMAIL_REQUIRED_ERROR   # adjust if you show format msg elsewhere
    LOGIN_ERROR_WITH_INVALID_PASSWORD = LOGIN_INVALID_CRED_ERROR
    SETTINGS_BTN=(By.ID, "settingsBtn")
    LOGOUT_BTN=(By.ID, "logoutBtn")

    @allure.step("Open Login Page")
    def open_login_page(self):
        self.open("/login.html")
        # Avoid depending on BasePage.go_to (may not exist in your version)

    @allure.step("Enter email: {1}")
    def enter_email_address(self, email):
        self.type(self.EMAIL_INPUT, email)

    @allure.step("Enter password")
    def enter_password(self, password):
        self.type(self.PASSWORD_INPUT, password)

    @allure.step("Click Login")
    def click_login_btn(self):
        self.click(self.LOGIN_BUTTON)

    @allure.step("click on Settings button")
    def click_settings_btn(self):
        if self.click(self.SETTINGS_BTN):
            self.click(self.SETTINGS_BTN)

    @allure.step("click on Logout button")
    def click_logout_btn(self):
        if self.click(self.LOGOUT_BTN):
            self.click(self.LOGOUT_BTN)

    # --- getters used by tests ---
    def login_verify(self):
        return self.text_of(self.LOGIN_SUCCESS_BANNER)

    def login_error_banner(self):
        return self.text_of(self.ERROR_BANNER)

    def email_required_error(self):
        return self.text_of(self.EMAIL_REQUIRED_ERROR)

    def password_required_error(self):
        return self.text_of(self.PASSWORD_REQUIRED_ERROR)

    def invalid_credentials_error(self):
        return self.text_of(self.LOGIN_INVALID_CRED_ERROR)

    def invalid_email_error(self):
        return self.text_of(self.LOGIN_INVALID_EMAIL_ERROR)

    def verify_settings_button_visible(self):
        return self.is_visible(self.SETTINGS_BTN)

    def verify_logout_button_visible(self):
        return self.is_visible(self.LOGOUT_BTN)