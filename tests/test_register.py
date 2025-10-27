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
test_data3 = read_excel("data/register_test_data.xlsx", sheet_name="Sheet3")


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
    def test_verify_system_prevents_duplicate_email_registration(
        self, driver, data, env, seed_registered_user
    ):
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
        assert actual.strip().lower() in (
            "email already exists",
            "user with this email already exists",
        )

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

        # wait for validation message to render
        rp.wait_visible(rp.EMAIL_VALIDATION_ERROR)

        error_text = rp.email_validation_error()
        assert error_text == "Enter a valid email address."

    @allure.story("Verify error message when email field is left blank")
    @pytest.mark.functional
    @pytest.mark.YWT26
    @pytest.mark.parametrize("data", test_data)
    def test_Verify_error_shown_when_email_field_is_blank(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()
        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])
        # Intentionally NOT entering email to trigger validation
        rp.enter_password(data["Password"])
        rp.enter_confirm_password(data["ConfirmPassword"])
        rp.click_register_button()

        error_text = rp.get_email_error_text()
        assert error_text == "Email is required."

    @allure.story("Verify error when confirm password does not match password")
    @pytest.mark.regression
    @pytest.mark.YWT12
    @pytest.mark.parametrize("data", test_data)
    def test_Verify_error_when_confirm_password_does_not_match_password(
        self, driver, data, env
    ):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()
        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])
        rp.enter_email_address(data["Email"])

        # Intentionally mismatch password vs confirm password from sheet
        rp.enter_password(data["Password"])
        rp.enter_confirm_password(data["ConfirmPassword"])
        rp.click_register_button()

        cnf_password_error_text = rp.get_cnf_password_error_text()
        assert cnf_password_error_text == "Passwords do not match."

    # --------- MERGED FROM branch YW_T53_Verify_FirstName_Accepts_Characters(A-Z)
    @allure.story("Verify first name accepts characters only")
    @pytest.mark.functional
    @pytest.mark.YWT53
    @pytest.mark.parametrize("data", test_data3)
    def test_Verify_first_name_accepts_characters_only(self, driver, data, env):
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

        first_name_error_text = rp.get_first_name_error_text()
        assert first_name_error_text == "Use 3–25 letters (A–Z only)."

    # --------- MERGED FROM main (SQL injection / invalid email scenario)
    @allure.story("Verify system prevents SQL injection in email field")
    @pytest.mark.smoke
    @pytest.mark.YWT49
    @pytest.mark.parametrize("data", test_data)
    def test_verify_system_prevent_sql_input_in_email(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()

        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])

        # Using Invalid_Email field which could include payload like "' OR 1=1 --"
        rp.enter_email_address(data["Invalid_Email"])
        rp.enter_password(data["Password"])
        rp.enter_confirm_password(data["ConfirmPassword"])

        # Wait for validation error before reading
        rp.wait_visible(rp.EMAIL_VALIDATION_ERROR)

        error_text = rp.email_validation_error()
        assert error_text == "Enter a valid email address."

    @allure.story("Verify user should get an error message of password is required")
    @pytest.mark.smoke
    @pytest.mark.YWT108
    @pytest.mark.parametrize("data", test_data)
    def test_verify_error_message_when_password_is_required(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()

        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])
        rp.enter_email_address(data["Email"])
        rp.click_register_button()

        password_required_text = rp.get_password_error_text()
        assert password_required_text=="Password is required."

        confirm_password_required_text = rp.get_cnf_password_error_text()
        assert confirm_password_required_text=="Confirm Password is required."