import pytest
import allure
import os
from core.wait import Waiter
from pages.home_page import HomePage
from pages.electronis_page import ElectronicsPage
from pages.login_page import LoginPage
from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/Login_test_data.xlsx")
@pytest.mark.parametrize("data", test_data)
class TestElectronics:

    def test_verify_user_able_sent_the_email_to_friend_about_phone(self, driver,data, env):
        """Test: Email a friend about used phone"""

        # 1. Go to website
        home_page = HomePage(driver, env)
        home_page.open_home()
        lp = LoginPage(driver, env)
        lp.open_login_page()

        lp.enter_email_address(data["EmailIDLogin"])
        lp.enter_password(data["PasswordLogin"])
        lp.click_login_btn()

        ep =ElectronicsPage(driver, env)
        Waiter(driver).visible(ep.ELECTRONICS_MENU)

         # 2. Navigate to Electronics > Cell Phones
        ep= ElectronicsPage(driver, env)
        ep.go_to_cell_phones()

        # 3. Select Used Phone
        ep.select_used_phone()
        ep.click_email_a_friend()

        ep.enter_friends_email_address(data["friend_email"])
        ep.enter_message_to_friend(data["message_txt"])
        ep.click_send_btn()

        assert_equals(
            "Your message has been sent.",
            ep.send_email_verification(),
            msg="email sent successfully successful"
        )

    def test_verify_without_login_validation_error_msg_for_friendsemail_and_youremailaddress(self, driver,data, env):
        """Test: without login, validation error msg for send email to friend and your email"""

        # 1. Go to website
        home_page = HomePage(driver, env)
        home_page.open_home()


        ep =ElectronicsPage(driver, env)
        Waiter(driver).visible(ep.ELECTRONICS_MENU)

         # 2. Navigate to Electronics > Cell Phones
        ep= ElectronicsPage(driver, env)
        ep.go_to_cell_phones()

        # 3. Select Used Phone
        ep.select_used_phone()
        ep.click_email_a_friend()
        ep.click_send_btn()
        Waiter(driver).visible(ep.VALIDATION_MSG_FOR_YOUR_EMAIL)
        assert_equals(
            "Enter friend's email",
            ep.validation_error_friends_email(),
            msg="validation msg verified"
        )

        assert_equals(
            "Enter your email",
            ep.validation_error_your_email(),
            msg="validation msg verified"
        )

    def test_verify_after_login_validation_error_msg_for_friends_email_and_your_email_address(self, driver,data, env):
        """Test: after login, validation error msg for send email to friend"""

        # 1. Go to website
        home_page = HomePage(driver, env)
        home_page.open_home()
        lp = LoginPage(driver, env)
        lp.open_login_page()

        lp.enter_email_address(data["EmailIDLogin"])
        lp.enter_password(data["PasswordLogin"])
        lp.click_login_btn()

        ep =ElectronicsPage(driver, env)
        Waiter(driver).visible(ep.ELECTRONICS_MENU)

         # 2. Navigate to Electronics > Cell Phones
        ep= ElectronicsPage(driver, env)
        ep.go_to_cell_phones()

        # 3. Select Used Phone
        ep.select_used_phone()
        ep.click_email_a_friend()
        ep.get_your_email()
        ep.click_send_btn()


        assert_equals(
            "Enter friend's email",
            ep.validation_error_friends_email(),
            msg="validation msg verified"
        )

        assert_equals(
            "test89test89@g.com",
            ep.get_your_email(),
            msg="both emails are matching"
        )



