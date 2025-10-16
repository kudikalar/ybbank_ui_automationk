from selenium.webdriver.common.by import By
from core.base_page import BasePage


class ForgotPasswordPage(BasePage):
    # ===== Locators =====
    FORGOT_PASSWORD_EMAIL_ADDRESS_TEXT_BOX = (By.ID, "email")
    FORGOT_PASSWORD_EMAIL_TEXT_FIELD_NAME = (By.XPATH, "//label[text()='Email Address *']")
    SEND_REST_LINK_BTN = (By.ID, "sendLink")
    SEND_OTP_BTN = (By.XPATH,"//button[@id='sendOtp']")
    BACK_TO_LOGIN_PAGE_HYPER_LINK = (By.XPATH, "//a[@class='link' and text()='Back to Login']")
    VERIFY_PALCE_HOLDER_TEXT = (By.XPATH, "//*[@placeholder='you@example.com']")
    VERIFY_PAGE_NAME = (By.XPATH, "//h1[@class='title' and text()='Forgot Password']")
    VALIDATE_TEXT1_INSTRUCTION = (By.XPATH, "//p[@class='sub']")
    VALIDATE_TEXT2_INSTRUCTION = (By.XPATH, "//div[@class='note']")
    VALIDATE_REMEMBER_TEXT = (By.XPATH, "//span[a[@class='link' and text()='Back to Login']]")
    DEMO_LINK = (By.ID, "demoLinkWrap")
    SUCCESS_MSG = (By.XPATH, "//p[@id='success']")

    # ===== OTP & Reset Section =====
    ENTER_OTP_TEXT_BOX = (By.ID, "otp")
    ENTER_OTP_TEXT_BOX_NAME = (By.XPATH, "//*[text()='Enter OTP *']")
    ENTER_OTP_TEXT_PLACE_HOLDER = (By.XPATH, "//input[@inputmode='numeric']")
    SUCCESS_MSG_OTP_SEND_TEXT = (By.XPATH, "//*[text()='If an account exists, an OTP has been sent.']")
    OTP_INPUT = (By.XPATH, "//input[@placeholder='Enter OTP' or @type='text']")

    NEW_PASSWORD_TEXT_FIELD_NAME = (By.XPATH, "//*[text()='New Password *']")
    NEW_PASSWORD_TEXT_BOX = (By.XPATH, "//input[@type='password' and @id='newPass']")
    NEW_PASSWORD_PLACE_HOLDER_TEXT = (By.XPATH, "//input[@type='password' and @id='newPass']")

    CONFIRM_PASSWORD_TEXT_FIELD_NAME = (By.XPATH, "//label[@for='confirmPass']")
    CONFIRM_PASSWORD_TEXT_BOX = (By.XPATH, "//input[@id='confirmPass']")
    CONFIRM_PASSWORD_PLACE_HOLDER_TEXT = (By.XPATH, "//input[@id='confirmPass']")

    VERIFY_OTP_AND_REST_BTN = (By.XPATH, "//button[@id='verifyAndReset']")
    OTP_TEXT_ELEMENT = (By.XPATH, "//span[@id='otpValue']")

    # ===== Constructor =====
    def __init__(self, driver, env):
        super().__init__(driver, env)

    # ===== Page Actions =====
    def open_forgot_password_page(self):
        self.open("/forgot")
        self.wait_url_contains("/forgot")
        self.wait_visible(self.SEND_REST_LINK_BTN)

    # ===== Verifications =====
    def verify_page_name(self):
        return self.text_of(self.VERIFY_PAGE_NAME)

    def enter_email_address(self, email):
        return self.type(self.FORGOT_PASSWORD_EMAIL_ADDRESS_TEXT_BOX, email)

    def verify_email_address_text_is_present(self):
        return self.is_visible(self.FORGOT_PASSWORD_EMAIL_ADDRESS_TEXT_BOX)

    def verify_email_text_box_name(self):
        return self.text_of(self.FORGOT_PASSWORD_EMAIL_TEXT_FIELD_NAME)

    def verify_place_holder_text_name(self):
        return self.attr(self.VERIFY_PALCE_HOLDER_TEXT, "placeholder")

    def verify_send_reset_link_btn_is_present(self):
        return self.is_visible(self.SEND_REST_LINK_BTN)

    def verify_send_rest_link_btn_txt_is_matching(self):
        return self.text_of(self.SEND_REST_LINK_BTN)

    def click_on_send_rest_link_btn_txt_is_matching(self):
        return self.click(self.SEND_REST_LINK_BTN)

    def verify_send_otp_btn_is_present(self):
        return self.is_visible(self.SEND_OTP_BTN)

    def verify_send_otp_btn_text_is_matching(self):
        return self.text_of(self.SEND_OTP_BTN)

    def click_on_send_otp_button(self):
        return self.click(self.SEND_OTP_BTN)

    def verify_intstrucation_text1(self):
        return self.text_of(self.VALIDATE_TEXT1_INSTRUCTION)

    def verify_instrucation_text2(self):
        return self.text_of(self.VALIDATE_TEXT2_INSTRUCTION)

    def validate_the_place_holder_text(self):
        return self.attr(self.VERIFY_PALCE_HOLDER_TEXT, "placeholder")

    def verify_remember_text(self):
        return self.text_of(self.VALIDATE_REMEMBER_TEXT)

    def verify_back_to_login_page(self):
        return self.text_of(self.BACK_TO_LOGIN_PAGE_HYPER_LINK)

    def verify_back_to_login_btn_present(self):
        return self.is_visible(self.BACK_TO_LOGIN_PAGE_HYPER_LINK)

    def verify_demo_link_present(self):
        return self.is_visible(self.DEMO_LINK)

    def verify_the_success_msg(self):
        return self.text_of(self.SUCCESS_MSG)

    # ===== OTP Section =====
    def enter_otp_text_box(self):
        return self.is_visible(self.ENTER_OTP_TEXT_BOX)

    def otp_text_box_name(self):
        return self.text_of(self.ENTER_OTP_TEXT_BOX_NAME)

    def get_place_holder_text_of_otp_text_box(self):
        return self.attr(self.ENTER_OTP_TEXT_PLACE_HOLDER, "placeholder")

    def new_password_text_field_name(self):
        return self.text_of(self.NEW_PASSWORD_TEXT_FIELD_NAME)

    def get_the_place_holder_Text(self):
        return self.attr(self.NEW_PASSWORD_PLACE_HOLDER_TEXT, "placeholder")

    def enter_new_password(self, newpassword):
        return self.type(self.NEW_PASSWORD_TEXT_BOX, newpassword)

    def enter_confirm_password(self, confirmpass):
        return self.type(self.CONFIRM_PASSWORD_TEXT_BOX, confirmpass)
