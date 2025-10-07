import allure
import pytest

from core.wait import Waiter
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/Login_test_data.xlsx")

@allure.feature("Login")
class TestLogin:

    @allure.story("Login with valid credentials")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_valid_credentials(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        lp = LoginPage(driver, env)
        lp.open_login_page()

        lp.enter_email_address(data["EmailIDLogin"])
        lp.enter_password(data["PasswordLogin"])
        lp.click_login_btn()

        Waiter(driver).visible(lp.LOGIN_VERIFY)
        assert_equals(
            "Welcome to our store",
            lp.login_verify(),
            msg="User should login successfully"
        )

    @allure.story("Login with invalid email")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_invalid_email(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        lp = LoginPage(driver, env)
        lp.open_login_page()

        lp.enter_email_address(data["InvalidEmail"])
        lp.enter_password(data["PasswordLogin"])
        lp.click_login_btn()

        Waiter(driver).visible(lp.LOGIN_ERROR_WITH_INVALID_EMAIL)
        assert_equals(
            "Please enter a valid email address.",
            lp.login_with_invalid_emailID_error(),
            msg="Should show invalid email error"
        )

    @allure.story("Login with invalid password")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_invalid_password(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        lp = LoginPage(driver, env)
        lp.open_login_page()

        lp.enter_email_address(data["EmailIDLogin"])
        lp.enter_password("WrongPassword123")
        lp.click_login_btn()

        Waiter(driver).visible(lp.LOGIN_ERROR_WITH_INVALID_PASSWORD)
        assert_equals(
            "The credentials provided are incorrect",
            lp.login_with_invalid_password_error(),
            msg="Should show incorrect credentials error"
        )

    @allure.story("Login with empty data")
    def test_login_with_empty_data(self, driver, env):
        hp = HomePage(driver, env)
        hp.open_home()

        lp = LoginPage(driver, env)
        lp.open_login_page()
        lp.click_login_btn()

        Waiter(driver).visible(lp.LOGIN_ERROR)
        assert_equals(
            "No customer account found",
            lp.login_with_empty_data_error(),
            msg="Should show account not found error"
        )

    @allure.story("Login with remember me checkbox")
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_remember_me(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        lp = LoginPage(driver, env)
        lp.open_login_page()

        lp.enter_email_address(data["EmailIDLogin"])
        lp.enter_password(data["PasswordLogin"])
        lp.click_remember_me_checkbox()
        lp.click_login_btn()

        Waiter(driver).visible(lp.LOGIN_VERIFY)
        assert_equals(
            "Welcome to our store",
            lp.login_verify(),
            msg="User should login with remember me checked"
        )
        #

