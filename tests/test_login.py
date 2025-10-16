import allure
import pytest

from core.wait import Waiter
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.assertions import assert_equals, assert_true
from utils.data_reader import read_excel

test_data = read_excel("data/register_test_data.xlsx")


# ---------- Precondition utils ----------
def _resolve_creds(data):
    """Extract credentials from either *Login or register keys."""
    email = data.get("EmailIDLogin") or data.get("Email") or data.get("EmailID")
    password = data.get("PasswordLogin") or data.get("Password")
    first = data.get("FirstName", "Auto")
    last = data.get("LastName", "User")
    if not email or not password:
        raise ValueError("Email or password missing in test data")
    return first, last, email, password


@allure.step("Ensure the user is registered (precondition)")
def ensure_registered(driver, env, data):
    hp = HomePage(driver, env)
    hp.open_home()
    first, last, email, password = _resolve_creds(data)

    # Check localStorage (browser-side storage)
    exists = driver.execute_script("""
        const key='yuvanbank_users';
        try {
          const users = JSON.parse(localStorage.getItem(key) || '[]');
          return users.some(u => (u.email || u.Email) === arguments[0]);
        } catch(e) { return false; }
    """, email)
    if exists:
        return  # already seeded

    # Otherwise register via UI
    rp = RegisterPage(driver, env)
    rp.open_register_page()
    rp.enter_first_name(first)
    rp.enter_last_name(last)
    rp.enter_email_address(email)
    rp.enter_password(password)
    rp.enter_confirm_password(password)
    rp.click_register_button()


# ---------- Tests ----------
@allure.feature("Login")
class TestLogin:

    @allure.story("Login with valid credentials")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_valid_credentials(self, driver, data, env):
        ensure_registered(driver, env, data)

        lp = LoginPage(driver, env)
        lp.open_login_page()

        _, _, email, password = _resolve_creds(data)
        lp.enter_email_address(email)
        lp.enter_password(password)
        lp.click_login_btn()

        Waiter(driver).visible(lp.SETTINGS_BTN)
        # assert_true(lp.verify_settings_button_visible())
        lp.click_settings_btn()
        # assert_true(lp.verify_logout_button_visible())
        lp.click_logout_btn()

    @allure.story("Login with empty fields")
    @pytest.mark.regression
    def test_login_with_empty_fields(self, driver, env):
        lp = LoginPage(driver, env)
        lp.open_login_page()
        lp.click_login_btn()

        # Top red banner + field-level errors per UI
        Waiter(driver).visible(lp.ERROR_BANNER)
        assert_equals("Please fix the errors above.", lp.login_error_banner(),
                      msg="Should show validation banner")

        Waiter(driver).visible(lp.EMAIL_REQUIRED_ERROR)
        Waiter(driver).visible(lp.PASSWORD_REQUIRED_ERROR)
        assert lp.email_required_error() == "Email is required."
        assert lp.password_required_error() == "Password is required."

    @allure.story("Login with invalid email")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_invalid_email(self, driver, data, env):
        ensure_registered(driver, env, data)

        lp = LoginPage(driver, env)
        lp.open_login_page()

        # Use obviously invalid email to trigger format validation
        lp.enter_email_address("not-an-email")
        lp.enter_password((data.get("PasswordLogin") or data.get("Password")))
        lp.click_login_btn()

        # Depending on your page, this can be either a format message or the banner.
        # Keep both to be resilient; assert the specific text if present.
        assert "Invalid email format." == lp.invalid_email_error()


    @allure.story("Login with invalid password")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_invalid_password(self, driver, data, env):
        ensure_registered(driver, env, data)

        lp = LoginPage(driver, env)
        lp.open_login_page()

        _, _, email, _ = _resolve_creds(data)
        lp.enter_email_address(email)
        lp.enter_password("WrongPassword123")
        lp.click_login_btn()

        Waiter(driver).visible(lp.LOGIN_INVALID_CRED_ERROR)
        assert_equals(
            "Invalid credentials. Please try again.",
            lp.invalid_credentials_error(),
            msg="Should show invalid credentials message"
        )

