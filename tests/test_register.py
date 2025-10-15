from dbm import error

import allure
import pytest, uuid
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/register_test_data.xlsx")

@allure.feature("Registration")
class TestRegister:

    @allure.story("YW-T2-Verify register functionality with valid data")
    @pytest.mark.smoke
    @pytest.mark.yw_t2
    @pytest.mark.parametrize("data", test_data)
    def test_verify_register_functionality_with_valid_data(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()
        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])
        rp.enter_email_address(data["Email"])
        rp.enter_password(data["Password"])
        rp.enter_confirm_password(data["ConfirmPassword"])
        rp.click_register_button()

        lp = LoginPage(driver, env)
        assert_equals(lp.welcome_message(), "Welcome Back")

    @allure.story("YW-T5-Verify_Password_and_Confirm_Password")
    @pytest.mark.funtional
    @pytest.mark.yw_t5
    @pytest.mark.parametrize("data", test_data)
    def test_verify_password_and_confirm_password(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()
        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])
        rp.enter_email_address(data["Email"])
        rp.enter_password(data["Password"])
        rp.enter_confirm_password(data["IncorrectPassword"])
        rp.click_register_button()

        rp.wait_visible(rp.PASSWORD_MISMATCH)
        error_text=rp.password_error()















