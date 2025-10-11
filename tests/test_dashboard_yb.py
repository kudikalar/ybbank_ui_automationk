import allure
import pytest
from pandas.core.arrays.categorical import contains
from core.wait import Waiter
from utils.data_reader import read_excel
from pages.Register_YB_Page import RegisterYBPage
from pages.Dashboard_YB_Page import DashboardPage

test_data = read_excel("data/yb_login_test_data.xlsx")
@allure.feature("Dashboard")
class TestDashboardYB:

    @allure.story("validate the dashboard elements")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_validate_the_dashboard_elements(self, driver, data, env):
        rp = RegisterYBPage(driver, env)
        rp.open_register_page()

        rp.enter_full_name_yb(data["full_name"])
        rp.enter_email_address(data["email"])
        rp.enter_password(data["password"])
        rp.enter_confirm_pwd(data["confirm_pwd"])
        rp.click_register_sign_btn()

        # Add dashboard verification after registration
        dp = DashboardPage(driver, env)
        Waiter(driver).visible(dp.ACCOUNTS_YB_BTN)

        # overview header and get text
        assert dp.over_view_header_present(), "overview header should be present on dashboard"
        overview_text = dp.over_view_header_text()
        assert overview_text == "View Account Overview"

        # Verify Bank Accounts is present on dashboard
        assert dp.is_bank_accounts_header_present(), "Bank Accounts header should be present on dashboard"
        bank_accounts_text = dp.get_bank_accounts_header_text()
        assert bank_accounts_text == "Bank Accounts"
        total_number_of_all_account_list = dp.get_initial_total_accounts()
        assert total_number_of_all_account_list == "0"


        # Verify bank balance header present on dashboard
        #welcome text verify
        assert dp.welcome_wish_text_present(), "Logout button is visible"
        verify_the_welcome_text = dp.verify_welcome_text()
        assert "Hello" in verify_the_welcome_text
        #no of bank accounts
        assert dp.is_bank_total_accounts_blc_header_present(), "Number of accounts header should be present on dashboard"
        bank_total_balance_text = dp.get_bank_total_accounts_blc_header_text()
        assert bank_total_balance_text == "Total Balance"
        total_account_blc = dp.get_initial_total_blc()
        assert total_account_blc == "₹0"

        # verify saving bank account header and get the text and validate
        assert dp.is_saving_accounts_blc_header_present(), "Savings Accounts header should be present on dashboard"
        saving_account_header_text = dp.get_savings_account_header_text()
        assert saving_account_header_text == "Savings Accounts"
        total_number_of_savings_account_blc = dp.get_savings_account_initial_total_blc()
        assert total_number_of_savings_account_blc == "0"

        # verify current bank account header and get the text and validate
        assert dp.is_current_accounts_blc_header_present(), "Current Accounts header should be present on dashboard"
        current_account_header_text = dp.get_current_account_header_text()
        assert current_account_header_text == "Current Accounts"
        total_number_of_current_account_list = dp.get_initial_current_accounts_list()
        assert total_number_of_current_account_list == "0"

        #add account from tip text
        assert dp.is_tip_add_account_present(), "The add account tip should be present"
        #tip_notice_text = dp.get_tip_text_from_add_account_text()
        #assert "Add Account" in tip_notice_text
        #assert tip_notice_text =="Add Account", "add account is present in tip text"



        # quick actions
        assert dp.quick_actions_header_present(), "quick actions header should be present on dashboard"
        quick_actions_text = dp.quick_actions_header_text()
        assert quick_actions_text == "Quick Actions"

        # add bank account
        assert dp.add_bank_account_header_present(), "Add Bank Account header should be present on dashboard"
        add_bank_account_text = dp.add_bank_accout_header_text()
        assert add_bank_account_text == "Add Bank Account"

        # view account overview
        assert dp.view_account_overview_header_present(), "View Account Overview header should be present on dashboard"
        view_account_overview_text = dp.view_account_overview_header_text()
        assert view_account_overview_text == "View Account Overview"

        #logout button
        assert dp.logout_btn_present, "Logout button is visible"
        verify_the_logout_text = dp.view_logout_btn_name()
        assert verify_the_logout_text == "Logout"

        #verify title and url
        assert dp.driver.title == "Simple Banking App (Demo)"
        assert dp.driver.current_url == "https://yuvanbank-qa-test.netlify.app/#dashboard"
