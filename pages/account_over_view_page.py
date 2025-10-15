from selenium.webdriver.common.by import By
from core.base_page import BasePage


class AccountOverViewPage(BasePage):
    ACCOUNT_OVERVVIEW_TEXT = (By.XPATH, "//h3[text()='Account Overview']")
    CLICK_ON_ALL_BTN = (By.XPATH, "//*[text()='All']")
    CLICK_ON_SAVING_BTN = (By.XPATH, "//div[contains(@class, 'tab') and contains(text(), 'Savings')]")
    CLICK_ON_CURRENT_BTN = (By.XPATH, "//div[@data-filter='CURRENT']")

    # FIXED LOCATORS
    VERIFY_BANK_FEILD_NAME_PRESENT = (By.XPATH, "//th[text()='Bank']")
    VERIFY_BANK_HOLDER_FIELD_PRESNET = (By.XPATH, "//th[text()='Holder']")
    VERIFY_ACCOUNT_FIELD_NAME_PRESENT = (By.XPATH, "//th[text()='Account #']")
    VERIFY_IFSC_FIELD_NAME_PRESENT = (By.XPATH, "//th[text()='IFSC']")
    VERIFY_TYPE_FIELD_NAME_PRESENT = (By.XPATH, "//th[text()='Type']")
    VERIFY_BALANCE_FIELD_NAME_PRESENT = (By.XPATH, "//th[text()='Balance']")
    VERIFY_CREATED_FEILD_NAME_PRESENT = (By.XPATH, "//th[text()='Created']")
    VERIFY_SUGESTION_TEXT_WITHOUT_ACCOUNT = (By.XPATH, "//td[text()='No accounts yet. Click Add to create one.']")
    VERIFY_INITIAL_ACCOUNT = (By.XPATH, "//span[text()='0 items']")
    VERIFY_ADD_BUTTON = (By.XPATH, "//*[text()='+ Add']")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_login_page(self):
        self.open("/#accounts")
        self.wait_url_contains("/#accounts")
        self.wait_visible(self.ACCOUNT_OVERVVIEW_TEXT)

    def verify_account_overview_text_present(self):
        return self.is_visible(self.ACCOUNT_OVERVVIEW_TEXT)

    def get_account_overview_text(self):
        return self.text_of(self.ACCOUNT_OVERVVIEW_TEXT)

    def click_on_all_btn_present(self):
        return self.is_visible(self.CLICK_ON_ALL_BTN)

    def verify_all_btn_txt(self):
        return self.text_of(self.CLICK_ON_ALL_BTN)

    def click_on_all_btn(self):
        return self.click(self.CLICK_ON_ALL_BTN)

    def verify_savinkings_btn_is_present(self):
        return self.is_visible(self.CLICK_ON_SAVING_BTN)

    def verify_saving_btn_text(self):
        return self.text_of(self.CLICK_ON_SAVING_BTN)

    def click_on_savings_btn(self):
        return self.click(self.CLICK_ON_SAVING_BTN)

    def verify_current_btn_is_present(self):
        return self.is_visible(self.CLICK_ON_CURRENT_BTN)

    def verify_current_btn_text(self):
        return self.text_of(self.CLICK_ON_CURRENT_BTN)

    def click_on_current_btn(self):
        return self.click(self.CLICK_ON_CURRENT_BTN)

    def verify_bank_text_name_present(self):
        return self.is_visible(self.VERIFY_BANK_FEILD_NAME_PRESENT)

    def verify_bank_text_name(self):
        return self.text_of(self.VERIFY_BANK_FEILD_NAME_PRESENT)

    def verify_holder_text_name_present(self):
        return self.is_visible(self.VERIFY_BANK_HOLDER_FIELD_PRESNET)

    def verify_holder_text_name(self):
        return self.text_of(self.VERIFY_BANK_HOLDER_FIELD_PRESNET)  # FIXED: Now returns holder text

    def verify_account_text_name_present(self):
        return self.is_visible(self.VERIFY_ACCOUNT_FIELD_NAME_PRESENT)

    def verify_account_text_name(self):
        return self.text_of(self.VERIFY_ACCOUNT_FIELD_NAME_PRESENT)

    def verify_ifsc_text_name_present(self):
        return self.is_visible(self.VERIFY_IFSC_FIELD_NAME_PRESENT)

    def verify_ifsc_text_name(self):
        return self.text_of(self.VERIFY_IFSC_FIELD_NAME_PRESENT)

    def verify_type_text_name_present(self):
        return self.is_visible(self.VERIFY_TYPE_FIELD_NAME_PRESENT)

    def verify_type_text_name(self):
        return self.text_of(self.VERIFY_TYPE_FIELD_NAME_PRESENT)

    def verify_balance_text_name_present(self):
        return self.is_visible(self.VERIFY_BALANCE_FIELD_NAME_PRESENT)

    def verify_blc_text_name(self):
        return self.text_of(self.VERIFY_BALANCE_FIELD_NAME_PRESENT)

    def verify_created_field_text_present(self):
        return self.is_visible(self.VERIFY_CREATED_FEILD_NAME_PRESENT)

    def verify_created_field_name(self):
        return self.text_of(self.VERIFY_CREATED_FEILD_NAME_PRESENT)

    def verify_suggestion_text_present(self):
        return self.is_visible(self.VERIFY_SUGESTION_TEXT_WITHOUT_ACCOUNT)

    def verify_suggestion_text_name(self):
        return self.text_of(self.VERIFY_SUGESTION_TEXT_WITHOUT_ACCOUNT)

    def verify_number_of_initial_accounts_present(self):
        return self.is_visible(self.VERIFY_INITIAL_ACCOUNT)

    def verify_number_accounts_text(self):
        return self.text_of(self.VERIFY_INITIAL_ACCOUNT)

    def verify_add_btn_is_present(self):
        return self.is_visible(self.VERIFY_ADD_BUTTON)

    def verify_add_btn_text(self):
        return self.text_of(self.VERIFY_ADD_BUTTON)

    def click_add_btn(self):
        return self.click(self.VERIFY_ADD_BUTTON)