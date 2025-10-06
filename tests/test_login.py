#verify login functionalitu with valid data
#verify login functionalitu with valid data

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.wait import Waiter
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.assertion import assert_equals


class TestLogin:

    BASE_URL = "https://demowebshop.tricentis.com/"

    def go_to_login_page(self, driver):
        hp = HomePage(driver, self.BASE_URL)
        hp.open_home()
        hp.click_login_link()
        return LoginPage(driver)

    def test_verify_login_functionality_with_valid_data(self, driver):
        lp = self.go_to_login_page(driver)
        lp.enter_email_address("test89test89@g.com")
        lp.enter_password("Test123")
        lp.click_login_btn()

        # Wait for success message
        # wait for element visible
        Waiter(driver).visible(lp.LOGIN_VERIFY)
        assert_equals(
            "Welcome to our store",
            lp.login_verify(),
            msg="user able to login"
        )


        assert "Welcome to our store" in lp.login_verify()

    def test_verify_login_functionality_with_empty_data(self, driver):
        lp = self.go_to_login_page(driver)
        lp.click_login_btn()

        # wait for element visible
        Waiter(driver).visible(lp.LOGIN_ERROR)
        assert_equals(
            "No customer account found",
            lp.login_with_empty_data_error(),
            msg="No user is not available with your creds"
        )

        #assert "No customer account found" in lp.login_with_empty_data_error()

    def test_verify_login_functionality_with_invalid_emailID(self, driver):
        lp = self.go_to_login_page(driver)
        lp.enter_email_address("test@gsggd")
        lp.enter_password("Testing")
        lp.click_login_btn()

        # wait for element visible
        Waiter(driver).visible(lp.LOGIN_ERROR_WITH_INVALID_EMAIL)
        assert_equals(
            "Please enter a valid email address.",
            lp.login_with_invalid_emailID_error(),
            msg="User is matching enter incorrect email ID"
        )

        #assert "Please enter a valid email address." in lp.login_with_invalid_emailID_error()

    def test_verify_login_functionality_with_invalid_password(self, driver):
        lp = self.go_to_login_page(driver)
        lp.enter_email_address("test456@t.com")
        lp.enter_password("jhgjhghgye")
        lp.click_login_btn()

        # wait for element visible
        Waiter(driver).visible(lp.LOGIN_ERROR_WITH_INVALID_PASSWORD)
        assert_equals(
            "The credentials provided are incorrect",
            lp.login_with_invalid_password_error(),
            msg="Your entered incorrect pwd"
        )


        #assert "The credentials provided are incorrect" in lp.login_with_invalid_password_error()

