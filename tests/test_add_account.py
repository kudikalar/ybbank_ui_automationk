from enum import verify

import allure
import pytest
from core.wait import Waiter
from utils.data_reader import read_excel
from pages.Register_YB_Page import RegisterYBPage
from pages.add_account_page import AddAccountPage
from pages.Dashboard_YB_Page import DashboardPage
import uuid
import random

test_data = read_excel("data/yb_login_test_data.xlsx")

@allure.feature("Add_bank_Account")
class TestAddAccountYB:
    @allure.story("validate the dashboard elements")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_verify_user_able_to_add_the_savings_bank_account(self, driver, data, env):
        rp = RegisterYBPage(driver, env)
        rp.open_register_page()

        rp.enter_full_name_yb(data["full_name"])
        rp.enter_email_address(data["email"])
        rp.enter_password(data["password"])
        rp.enter_confirm_pwd(data["confirm_pwd"])
        rp.click_register_sign_btn()

        dp = DashboardPage(driver, env)
        Waiter(driver).visible(dp.ADD_ACCOUNT_YB_BTN)
        dp.click_add_account_btn()

        ac = AddAccountPage(driver, env)
        Waiter(driver).visible(ac.ADD_BANK_TITLE)
        assert ac.add_bank_page_title_present()

        # enter bank name
        assert ac.verify_bank_input_field_name_present(), "bank name field present"
        verify_bank_name_field = ac.bank_account_text_Name()
        assert verify_bank_name_field == "Bank Name"
        ac.bank_input_text_box(data["bank_name"])

        # account holder name
        assert ac.verify_account_holder_input_field_name_present(), "verifying the account holder text box name"
        verify_input_text_box = ac.account_holder_input_field_name()
        assert verify_input_text_box == "Account Holder"
        ac.account_holder_input_text_box(data["account_holder_name"])

        # enter the account number
        assert ac.verify_account_number_text_box_name_present()
        verify_input_account_number = ac.account_number_field_name()
        assert verify_input_account_number == "Account Number"
        # Generate unique account number with specific last 4 digits
        base_account_number = str(data["account_number"])[:-4]  # Get all but last 4 digits
        last_four_digits = str(random.randint(1000, 9999))  # Random last 4 digits
        unique_account_number = base_account_number + last_four_digits
        ac.account_number_input_text_box(unique_account_number)

        # IFSC CODE
        assert ac.verify_ifsc_text_box_field_name_present()
        verify_ifsc_field_name = ac.ifsc_text_box_field_name()
        assert verify_ifsc_field_name == "IFSC"
        ac.ifsc_input_field_text_box(data["ifsc_code"])

        # select savings from type drop down
        assert ac.verify_type_drop_down_name_present()
        verify_type_dropdown_name = ac.type_drop_down_name()
        assert verify_type_dropdown_name == "Type"
        ac.select_the_saving_options_from_type_dropdown()

        # openings balance
        assert ac.verify_openings_blc_text_field_name_present()
        verify_opening_blc_text_field_name = ac.openings_account_blc()
        assert verify_opening_blc_text_field_name == "Opening Balance (₹)"
        ac.opening_blc_input_text_box(str(data["Opening_balance"]))

        assert driver.title =="Simple Banking App (Demo)"
        assert driver.current_url == "https://yuvanbank-qa-test.netlify.app/#add-account"

        # click on save button
        ac.click_on_save_btn()

    test_data = read_excel("data/yb_login_test_data.xlsx")
    @allure.story("validate the dashboard elements")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_verify_user_able_to_add_the_current_bank_account(self, driver, data, env):
        rp = RegisterYBPage(driver, env)
        rp.open_register_page()

        rp.enter_full_name_yb(data["full_name"])
        rp.enter_email_address(data["email"])
        rp.enter_password(data["password"])
        rp.enter_confirm_pwd(data["confirm_pwd"])
        rp.click_register_sign_btn()

        dp = DashboardPage(driver, env)
        Waiter(driver).visible(dp.ADD_ACCOUNT_YB_BTN)
        dp.click_add_account_btn()

        ac = AddAccountPage(driver, env)
        Waiter(driver).visible(ac.ADD_BANK_TITLE)
        assert ac.add_bank_page_title_present()
        # enter bank name
        ac.bank_input_text_box(data["bank_name"])

        # account holder name/
        ac.account_holder_input_text_box(data["account_holder_name"])

        # enter the account number
        # Generate unique account number with specific last 4 digits
        base_account_number = str(data["account_number"])[:-4]  # Get all but last 4 digits
        last_four_digits = str(random.randint(1000, 9999))  # Random last 4 digits
        unique_account_number = base_account_number + last_four_digits
        ac.account_number_input_text_box(unique_account_number)
        # IFSC CODE
        ac.ifsc_input_field_text_box(data["ifsc_code"])
        # select savings from type drop down
        ac.select_the_current_option_from_type_dropdown()
        # openings balance
        ac.opening_blc_input_text_box(str(data["Opening_balance"]))
        # click on save button
        ac.click_on_save_btn()