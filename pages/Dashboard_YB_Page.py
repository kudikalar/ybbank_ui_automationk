from selenium.webdriver.common.by import By
from core.base_page import BasePage


class DashboardPage(BasePage):
    DASHBOARD_YB_BTN = (By.XPATH, "//*[text()='Dashboard']")
    ACCOUNTS_YB_BTN = (By.XPATH, "//*[text()='Accounts']")
    ADD_ACCOUNT_YB_BTN = (By.XPATH, "//*[text()='Add Account']")
    LOGOUT_BTN_YB = (By.XPATH, "//*[text()='Logout']")

    # Overview related
    OVER_VIEW_TEXT = (By.XPATH, "//h3[text()='Overview']")
    BANK_ACCOUNT_HEADER_NAME = (By.XPATH, "//*[text()='Bank Accounts']")
    TOTAL_BANK_ACCOUNT_LIST = (By.ID, "kpiAccounts")
    BANK_ACCOUNT_NAME = (By.XPATH, "//*[text()='Total Balance']")
    TOTAL_ACCOUNT_BLC = (By.ID, "kpiBalance")
    SAVING_ACCOUNT = (By.XPATH, "//*[text()='Savings Accounts']")
    NUMBER_SAVINGS_ACCOUNTS = (By.ID, "kpiSavings")
    CURRENT_ACCOUNTS = (By.XPATH, "//*[text()='Current Accounts']")
    NUMBER_CURRENT_ACCOUNTS = (By.ID, "kpiCurrent")  # Fixed: changed from XPATH to ID
    ADD_ACCOUNT = (By.XPATH, "//*[@id='dashboardSection']/div[1]/div[2]/div[2]/strong")
    ADD_ACCOUNT_BTN_TIP = (By.XPATH,"//div[contains(@class, 'notice')]//strong[text()='Add Account']")
    ADD_ACCOUNT_TIP_NOTICE_TEXT =(By.XPATH,"//div[contains(@class, 'notice')]")
    WELCOME_WISH_TEXT = (By.ID,"welcome")

    # Quick Actions
    QUICK_ACTIONS_VERIFY = (By.XPATH, "//*[text()='Quick Actions']")
    ADD_BANK_ACCOUNT = (By.XPATH, "//*[text()='Add Bank Account']")
    VIEW_ACCOUNT_OVERVIEW = (By.XPATH, "//*[text()='View Account Overview']")



    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_register_page(self):
        self.open("/#dashboard")
        self.wait_url_contains("#dashboard")
        self.wait_visible(self.DASHBOARD_YB_BTN)

    def click_dashboard_btn(self):
        self.click(self.DASHBOARD_YB_BTN)

    def click_accounts_btn(self):
        self.click(self.ACCOUNTS_YB_BTN)

    def click_add_account_btn(self):
        self.click(self.ADD_ACCOUNT_YB_BTN)

    def click_logout_btn(self):
        self.click(self.LOGOUT_BTN_YB)
    #bank account
    def is_bank_accounts_header_present(self):
        return self.is_visible(self.BANK_ACCOUNT_HEADER_NAME)
    def get_bank_accounts_header_text(self):
        return self.text_of(self.BANK_ACCOUNT_HEADER_NAME)
    def get_initial_total_accounts(self):
        return self.text_of(self.TOTAL_BANK_ACCOUNT_LIST)

    #overview TEXT
    def over_view_header_present(self):
        return self.is_visible(self.VIEW_ACCOUNT_OVERVIEW)
    def over_view_header_text(self):
        return self.text_of(self.VIEW_ACCOUNT_OVERVIEW)
    #total balance
    def is_bank_total_accounts_blc_header_present(self):
        return self.is_visible(self.BANK_ACCOUNT_NAME)
    def get_bank_total_accounts_blc_header_text(self):
        return self.text_of(self.BANK_ACCOUNT_NAME)
    def get_initial_total_blc(self):
        return self.text_of(self.TOTAL_ACCOUNT_BLC)

    def is_saving_accounts_blc_header_present(self):
        return self.is_visible(self.SAVING_ACCOUNT)
    def get_savings_account_header_text(self):
        return self.text_of(self.SAVING_ACCOUNT)
    def get_savings_account_initial_total_blc(self):
        return self.text_of(self.NUMBER_SAVINGS_ACCOUNTS)
    #current account
    def is_current_accounts_blc_header_present(self):
        return self.is_visible(self.CURRENT_ACCOUNTS)
    def get_current_account_header_text(self):
        return self.text_of(self.CURRENT_ACCOUNTS)
    def get_initial_current_accounts_list(self):
            return self.text_of(self.NUMBER_CURRENT_ACCOUNTS)

    def is_tip_add_account_present(self):
        return self.is_visible(self.ADD_ACCOUNT_BTN_TIP)
    def get_tip_text_from_add_account_text(self):
        return self.text_of(self.ADD_ACCOUNT_TIP_NOTICE_TEXT)

    #WECOME WISH
    def welcome_wish_text_present(self):
        return self.is_visible(self.WELCOME_WISH_TEXT)
    def verify_welcome_text(self):
        return self.text_of(self.WELCOME_WISH_TEXT)

        #aCTIONS

    def quick_actions_header_present(self):
        return self.is_visible(self.QUICK_ACTIONS_VERIFY)
    def quick_actions_header_text(self):
        return self.text_of(self.QUICK_ACTIONS_VERIFY)

    def add_bank_account_header_present(self):
        return self.is_visible(self.ADD_BANK_ACCOUNT)
    def add_bank_accout_header_text(self):
        return self.text_of(self.ADD_BANK_ACCOUNT)

    def view_account_overview_header_present(self):
        return self.is_visible(self.VIEW_ACCOUNT_OVERVIEW)
    def view_account_overview_header_text(self):
        return self.text_of(self.VIEW_ACCOUNT_OVERVIEW)

    def logout_btn_present(self):
        return self.is_visible(self.LOGOUT_BTN_YB)
    def view_logout_btn_name(self):
        return self.text_of(self.LOGOUT_BTN_YB)



