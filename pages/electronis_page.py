from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.base_page import BasePage


class ElectronicsPage(BasePage):
    # Real-world locators for demo webshop
    ELECTRONICS_MENU = (By.XPATH, "//a[contains(text(),'Electronics')]")
    CELL_PHONES_MENU = (By.XPATH, "//a[contains(text(),'Cell phones')]")
    USED_PHONE_PRODUCT = (By.XPATH, "//a[contains(text(),'Used phone')]")
    EMAIL_FRIEND_BTN = (By.XPATH, "//input[@value='Email a friend']")
    FRIEND_EMAIL_FIELD = (By.ID, "FriendEmail")
    YOUR_EMAIL_TEXT_BTN =(By.ID,"YourEmailAddress")
    MESSAGE_FIELD = (By.ID, "PersonalMessage")
    SEND_EMAIL_BTN = (By.NAME, "send-email")
    VERIFY_SEND_EMAIL =(By.XPATH,"//div[contains(text(),'Your message has been sent.')]")
    VALIDATION_MSG_FOR_FRIEND_EMAIL =(By.XPATH,"//span[contains(text(),'Enter friend')]")
    VALIDATION_MSG_FOR_YOUR_EMAIL = (By.XPATH,"//span[contains(text(),'Enter your email')]")


    def __init__(self, driver, env):
        super().__init__(driver, env)
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_cell_phones(self):
        """Hover Electronics -> Click Cell Phones"""
        # Hover on Electronics menu
        electronics = self.wait.until(EC.element_to_be_clickable(self.ELECTRONICS_MENU))
        ActionChains(self.driver).move_to_element(electronics).perform()

        # Click Cell Phones
        cell_phones = self.wait.until(EC.element_to_be_clickable(self.CELL_PHONES_MENU))
        cell_phones.click()
        print("Navigated to Cell Phones")

    def select_used_phone(self):
        """Click on Used Phone product"""
        used_phone = self.wait.until(EC.element_to_be_clickable(self.USED_PHONE_PRODUCT))
        used_phone.click()

    def click_email_a_friend(self):
        friedn_email =self.wait.until(EC.element_to_be_clickable(self.EMAIL_FRIEND_BTN))
        friedn_email.click()


    def enter_friends_email_address(self, email):
        self.type(self.FRIEND_EMAIL_FIELD, email)

    def get_your_email(self):
        """Get the value from Your Email field"""
        try:
            # Get the element and return its value attribute
            email_element = self.wait.until(EC.visibility_of_element_located(self.YOUR_EMAIL_TEXT_BTN))
            return email_element.get_attribute("value")
        except Exception as e:
            print(f"Error getting email: {e}")
            return None


    def enter_message_to_friend(self, message):
        self.type(self.MESSAGE_FIELD, message)

    def click_send_btn(self):
        self.click(self.SEND_EMAIL_BTN)

    #validations
    def send_email_verification(self): return self.text_of(self.VERIFY_SEND_EMAIL)
    def validation_error_friends_email(self):
        return self.text_of(self.VALIDATION_MSG_FOR_FRIEND_EMAIL)
    def validation_error_your_email(self):
        return self.text_of(self.VALIDATION_MSG_FOR_YOUR_EMAIL)

    def get_the_email(self):
        """Get the value from Your Email field"""
        return self.get_attribute(self.YOUR_EMAIL_TEXT_BTN, "value")

