from selenium.webdriver.common.by import By
from core.base_page import BasePage

class AddAccountPage(BasePage):
    ADD_BANK_TITLE = (By.XPATH,"//h3[text()='Add Bank Account']")
    VERIFY_BANK_INPUT_FIELD_NAME = (By.XPATH,"//*[text()='Bank Name']")
    BANK_NAME_INPUT_TEXT_BOX = (By.ID,"bankName")
    VERIFY_ACCOUNT_HOLDER_INPUT_FIELD_NAME = (By.XPATH,"//*[text()='Account Holder']")
    ACCOUNT_HOLDER_INPUT_TEXT_BOX =(By.ID,"holder")
    VERIFY_ACCOUNT_NUMBER_TEXT_FIELD_NAME = (By.XPATH,"//*[text()='Account Number']")
    ACCOUNT_NUMBER_INPUT_TEXT_BOX = (By.ID,"accNumber")
    VERIFY_IFSC_FIELD_NAME = (By.XPATH,"//*[text()='IFSC']")
    IFSC_FIELD_INPUT_TEXT_BOX = (By.ID,"ifsc")
    VERIFY_TYPE_DROP_DOWN_NAME = (By.XPATH,"//label[@for='type']")
    SELECT_DROP_DOWN = (By.ID,"type")
    OPENINGS_BLC_TEXT_FIELD_NAME = (By.XPATH,"//label[@for='balance']")
    OPENINGS_BLC_INPUT_FIELD_BOX = (By.ID,"balance")
    CLICK_ON_SAVE_BTN = (By.XPATH,"//*[text()='Save Account']")
    ADD_BUTTON = (By.XPATH,"//*[text()='+ Add']")


    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_login_page(self):
        self.open("#add-account")
        self.wait_url_contains("#add-account")
        self.wait_visible(self.ADD_BANK_TITLE)


    def add_bank_page_title_present(self):
        return self.is_visible(self.ADD_BANK_TITLE)

    def verify_bank_input_field_name_present(self):
        return self.is_visible(self.VERIFY_BANK_INPUT_FIELD_NAME)
    def bank_account_text_Name(self):
        return self.text_of(self.VERIFY_BANK_INPUT_FIELD_NAME)
    def bank_input_text_box(self, bank_name):
        return self.type(self.BANK_NAME_INPUT_TEXT_BOX, bank_name)

    def verify_account_holder_input_field_name_present(self):
        return self.is_visible(self.VERIFY_ACCOUNT_HOLDER_INPUT_FIELD_NAME)
    def account_holder_input_field_name(self):
        return self.text_of(self.VERIFY_ACCOUNT_HOLDER_INPUT_FIELD_NAME)
    def account_holder_input_text_box(self, account_holder_name):
        return self.type(self.ACCOUNT_HOLDER_INPUT_TEXT_BOX, account_holder_name)

    def verify_account_number_text_box_name_present(self):
        return self.is_visible(self.VERIFY_ACCOUNT_NUMBER_TEXT_FIELD_NAME)
    def account_number_field_name(self):
        return self.text_of(self.VERIFY_ACCOUNT_NUMBER_TEXT_FIELD_NAME)
    def account_number_input_text_box(self, account_number):
        return self.type(self.ACCOUNT_NUMBER_INPUT_TEXT_BOX, account_number)

    def verify_ifsc_text_box_field_name_present(self):
        return self.is_visible(self.VERIFY_IFSC_FIELD_NAME)
    def ifsc_text_box_field_name(self):
        return self.text_of(self.VERIFY_IFSC_FIELD_NAME)
    def ifsc_input_field_text_box(self, ifsc_code):
        return self.type(self.IFSC_FIELD_INPUT_TEXT_BOX, ifsc_code)

    def verify_type_drop_down_name_present(self):
        return self.is_visible(self.VERIFY_TYPE_DROP_DOWN_NAME)
    def type_drop_down_name(self):
        return self.text_of(self.VERIFY_TYPE_DROP_DOWN_NAME)
    def select_the_saving_options_from_type_dropdown(self):
        return self.select_by_text(self.SELECT_DROP_DOWN, "Savings")
    def select_the_current_option_from_type_dropdown(self):
        return self.select_by_text(self.SELECT_DROP_DOWN, "Current")

    def verify_openings_blc_text_field_name_present(self):
        return self.is_visible(self.OPENINGS_BLC_TEXT_FIELD_NAME)
    def openings_account_blc(self):
        return self.text_of(self.OPENINGS_BLC_TEXT_FIELD_NAME)
    def opening_blc_input_text_box(self, openings_blc):
        return self.type(self.OPENINGS_BLC_INPUT_FIELD_BOX, openings_blc)

    def verify_add_button_present(self):
        return self.is_visible(self.ADD_BUTTON)
    def verify_add_button_text(self):
        return self.text_of(self.ADD_BUTTON)
    def click_on_the_add_btn(self):
        return self.click(self.ADD_BUTTON)

    def click_on_save_btn(self):
        return self.click(self.CLICK_ON_SAVE_BTN)


