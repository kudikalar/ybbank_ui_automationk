from selenium.webdriver.common.by import By
from core.base_page import BasePage


class ForgotPasswordPage(BasePage):
    FORGOT_PWD_LINK = (By.XPATH, "//a[text()='Forgot password?']")
    VERIFY_PAGE_RECOVER_PWD = (By.XPATH, "//h1[text()='Password recovery']")
    EMAIL_INPUT = (By.ID, "Email")
    SUBMIT_BTN = (By.XPATH, "//input[@value='Recover']")
    CONFIRM_MSG = (By.CSS_SELECTOR, "div.result")  # success message
    INVALID_EMAIL_ERROR = (By.XPATH, "/html/body/div[4]/div[1]/div[4]/div[2]/div/div[2]/form/div[1]/div/div/span[2]")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_forgot_password_page(self):
        self.open("/passwordrecovery")
        self.wait_url_contains("/passwordrecovery")
        self.wait_visible(self.VERIFY_PAGE_RECOVER_PWD)

    # ---- Action Methods ----
    def enter_recover_email_address(self, email):
        self.type(self.EMAIL_INPUT, email)

    def click_recover_button(self):
        self.click(self.SUBMIT_BTN)

    # ---- Verification Methods ----
    def get_confirmation_message(self):
        return self.text_of(self.CONFIRM_MSG)

    def get_invalid_email_error(self):
        return self.text_of(self.INVALID_EMAIL_ERROR)
