from enum import verify
import allure
import pytest
from core.wait import Waiter
from utils.data_reader import read_excel
from pages.Register_YB_Page import RegisterYBPage
from pages.add_account_page import AddAccountPage
from pages.Dashboard_YB_Page import DashboardPage
from pages.account_over_view_page import AccountOverViewPage
import uuid
import random

test_data = read_excel("data/yb_login_test_data.xlsx")


@allure.feature("Account_Over_view")
class TestAccount_Over_view:
    @allure.story("Account over view page")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_verify_user_able_to_add_the_current_bank_account_from_over_view_page(self, driver, data, env):
        rp = RegisterYBPage(driver, env)
        rp.open_register_page()

        rp.enter_full_name_yb(data["full_name"])
        rp.enter_email_address(data["email"])
        rp.enter_password(data["password"])
        rp.enter_confirm_pwd(data["confirm_pwd"])
        rp.click_register_sign_btn()
        dp = DashboardPage(driver, env)
        Waiter(driver).visible(dp.ACCOUNTS_YB_BTN)
        dp.click_accounts_btn()


        aop = AccountOverViewPage(driver, env)

        Waiter(driver).visible(aop.ACCOUNT_OVERVVIEW_TEXT)

        # Verify All button
        assert aop.click_on_all_btn_present()
        text_all_btn = aop.verify_all_btn_txt()
        assert text_all_btn == 'All'
        aop.click_on_all_btn()

        # Verify field names
        assert aop.verify_bank_text_name_present()
        bank_text = aop.verify_bank_text_name()
        assert bank_text == 'Bank'

        assert aop.verify_holder_text_name_present()
        holder_text_name = aop.verify_holder_text_name()
        assert holder_text_name == 'Holder'

        assert aop.verify_account_text_name_present()
        account_text_name = aop.verify_account_text_name()
        assert account_text_name == 'Account #'

        assert aop.verify_ifsc_text_name_present()
        ifsc_code_name = aop.verify_ifsc_text_name()
        assert ifsc_code_name == 'IFSC'

        assert aop.verify_type_text_name_present()
        assert aop.verify_balance_text_name_present()
        assert aop.verify_created_field_text_present()
        assert aop.verify_suggestion_text_present()
        aop.click_add_btn()

        # Add account
        ac = AddAccountPage(driver, env)
        # enter bank name
        ac.bank_input_text_box(data["bank_name"])

        # account holder name
        ac.account_holder_input_text_box(data["account_holder_name"])

        # enter the account number
        # Generate unique account number with specific last 4 digits
        base_account_number = str(data["account_number"])[:-4]  # Get all but last 4 digits
        last_four_digits = str(random.randint(1000, 9999))  # Random last 4 digits
        unique_account_number = base_account_number + last_four_digits
        ac.account_number_input_text_box(unique_account_number)

        # IFSC CODE
        ac.ifsc_input_field_text_box(data["ifsc_code"])

        # select current from type drop down
        ac.select_the_current_option_from_type_dropdown()

        # openings balance
        ac.opening_blc_input_text_box(str(data["Opening_balance"]))

        # click on save button
        ac.click_on_save_btn()

    @allure.feature("Account_Over_view")
    @allure.story("Account over view page")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_verify_user_able_to_add_the_savings_bank_account_from_over_view_page(self, driver, data, env):
        rp = RegisterYBPage(driver, env)
        rp.open_register_page()

        rp.enter_full_name_yb(data["full_name"])
        rp.enter_email_address(data["email"])
        rp.enter_password(data["password"])
        rp.enter_confirm_pwd(data["confirm_pwd"])
        rp.click_register_sign_btn()
        dp = DashboardPage(driver, env)
        Waiter(driver).visible(dp.ACCOUNTS_YB_BTN)
        dp.click_accounts_btn()

        aop = AccountOverViewPage(driver, env)

        Waiter(driver).visible(aop.ACCOUNT_OVERVVIEW_TEXT)

        # Verify All button
        assert aop.click_on_all_btn_present()
        text_all_btn = aop.verify_all_btn_txt()
        assert text_all_btn == 'All'
        aop.click_on_all_btn()

        # Verify field names
        assert aop.verify_bank_text_name_present()
        bank_text = aop.verify_bank_text_name()
        assert bank_text == 'Bank'

        assert aop.verify_holder_text_name_present()
        holder_text_name = aop.verify_holder_text_name()
        assert holder_text_name == 'Holder'

        assert aop.verify_account_text_name_present()
        account_text_name = aop.verify_account_text_name()
        assert account_text_name == 'Account #'

        assert aop.verify_ifsc_text_name_present()
        ifsc_code_name = aop.verify_ifsc_text_name()
        assert ifsc_code_name == 'IFSC'

        assert aop.verify_type_text_name_present()
        assert aop.verify_balance_text_name_present()
        assert aop.verify_created_field_text_present()
        assert aop.verify_suggestion_text_present()
        aop.click_add_btn()

        # Add account
        ac = AddAccountPage(driver, env)
        # enter bank name
        ac.bank_input_text_box(data["bank_name"])

        # account holder name
        ac.account_holder_input_text_box(data["account_holder_name"])

        # enter the account number
        # Generate unique account number with specific last 4 digits
        base_account_number = str(data["account_number"])[:-4]  # Get all but last 4 digits
        last_four_digits = str(random.randint(1000, 9999))  # Random last 4 digits
        unique_account_number = base_account_number + last_four_digits
        ac.account_number_input_text_box(unique_account_number)

        # IFSC CODE
        ac.ifsc_input_field_text_box(data["ifsc_code"])

        # select current from type drop down
        ac.select_the_saving_options_from_type_dropdown()

        # openings balance
        ac.opening_blc_input_text_box(str(data["Opening_balance"]))

        # click on save button
        ac.click_on_save_btn()