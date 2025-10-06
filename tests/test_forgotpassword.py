import allure
import pytest

from core.wait import Waiter
from pages.home_page import HomePage
from pages.forgot_password_page1 import ForgotPasswordPage
from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/register_test_data.xlsx")


@allure.feature("ForgotPassword")
class TestForgotPassword:

    @allure.story("Verify forgot password with valid email")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_verify_forgot_password_functionality_with_valid_data(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        # Navigate to forgot password page
        fp = ForgotPasswordPage(driver, env)
        fp.open_forgot_password_page()

        # Enter valid email and click Recover
        fp.enter_recover_email_address(data["EmailIDLogin"])
        fp.click_recover_button()

        # Wait and verify confirmation message
        Waiter(driver).visible(fp.CONFIRM_MSG)
        assert_equals(
            "Email with instructions has been sent to you.",
            fp.get_confirmation_message(),
            msg="Password recovery email sent successfully"
        )

    @allure.story("Verify forgot password with invalid email")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", test_data)
    def test_verify_forgot_password_functionality_with_invalid_data(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        # Navigate to forgot password page
        fp = ForgotPasswordPage(driver, env)
        fp.open_forgot_password_page()

        # Enter invalid email and click Recover
        fp.enter_recover_email_address(data["InvalidEmail"])
        fp.click_recover_button()

        # Wait and verify invalid email error message
        Waiter(driver).visible(fp.INVALID_EMAIL_ERROR)
        assert_equals(
            "Wrong email",
            fp.get_invalid_email_error(),
            msg="Proper error not displayed for invalid email"
        )
