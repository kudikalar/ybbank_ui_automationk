import pytest
import allure

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.assertions import assert_equals
from utils.data_reader import read_excel
# Read by sheet name
test_data = read_excel("data/register_test_data.xlsx", sheet_name="Sheet1")
test_data1 = read_excel("data/register_test_data.xlsx", sheet_name=2)

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

    @allure.story("YW-T6-Verify system prevents duplicate email registration")
    @pytest.mark.regression
    @pytest.mark.yw_t6
    @pytest.mark.parametrize("data", test_data1)
    @pytest.mark.parametrize("seed_registered_user", test_data1, indirect=True)
    def test_verify_system_prevents_duplicate_email_registration(self, driver, data, env, seed_registered_user):
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

        actual = rp.get_email_already_exists_text()
        assert actual.strip().lower() in ("email already exists", "user with this email already exists")








    @allure.story("YW-T3-Verify register functionality with Invalid Email")
    @pytest.mark.functional
    @pytest.mark.yw_t3
    @pytest.mark.parametrize("data", test_data)
    def test_verify_register_functionality_with_invalid_email(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()
        rp.enter_first_name("")
        rp.enter_last_name("")
        rp.enter_password("")
        rp.enter_confirm_password("")
        rp.enter_email_address(data["Invalid_Email"])
        rp.wait_visible(rp.EMAIL_VALIDATION_ERROR)

        error_text = rp.email_validation_error()
        assert error_text == "Enter a valid email address."