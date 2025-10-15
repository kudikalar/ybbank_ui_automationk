import allure
import pytest
from core.wait import Waiter
from pages.ForgotPasswordPage_Yuvan_bank import ForgotPasswordPage
from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/ForgotPassword.xlsx")
@allure.feature("Forgot password")
class TestLogin:
    @allure.story("Forgot password")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_validate_Forgot_Valid_Email_Submission_successful_msg(self,data, driver, env):
        fp = ForgotPasswordPage(driver, env)
        fp.open_forgot_password_page()
        Waiter(driver).visible(fp.SEND_REST_LINK_BTN)

        assert "Forgot Password — Yuvan Bank" in driver.title
        assert "https://yuvanbank-qa-r1-test.netlify.app/forgot" in driver.current_url
        #verifying the button is visible and text boxes are present
        fp.verify_email_address_text_is_present()
        fp.verify_send_reset_link_btn_is_present()
        fp.verify_send_otp_btn_is_present()
        fp.verify_back_to_login_btn_present()

        #verified the all text field, title and instructions are matching
        assert_equals("Forgot Password",fp.verify_page_name(),msg="User land on the forgot password page")
        assert_equals("Email Address *",fp.verify_email_text_box_name(),"Email address field name is matching")
        assert_equals("you@example.com",fp.verify_place_holder_text_name(),"place holder text is matching")
        assert_equals("Send reset link",fp.verify_send_rest_link_btn_txt_is_matching(),"rest btn text is matching")
        assert_equals("Send OTP",fp.verify_send_otp_btn_text_is_matching(),"send otp text matching")
        assert_equals("Back to Login",fp.verify_back_to_login_page(),"Back to login page link text matching")
        assert_equals("Please enter the email address that was used at the time of account creation.",fp.verify_intstrucation_text1(),"instruction text matching")
        assert_equals("We’ll never reveal whether an email is registered. Messages are neutral.",fp.verify_instrucation_text2(),"instruction text is matching")
        assert_equals("Remembered your password? Back to Login",fp.verify_remember_text(),"remember me text is matching")

        fp.enter_email_address(data["fpw_yb_valid"])
        fp.click_on_send_rest_link_btn_txt_is_matching()
        Waiter(driver).visible(fp.SUCCESS_MSG)
        assert_equals("Password reset link sent successfully.",fp.verify_the_success_msg(),"Rest link is successfully sent to the user")

    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_validate_Forgot_Valid_Email_Submission_successful_send_otp_msg(self,data, driver, env):
        fp = ForgotPasswordPage(driver, env)
        fp.open_forgot_password_page()
        Waiter(driver).visible(fp.SEND_REST_LINK_BTN)

        assert "Forgot Password — Yuvan Bank" in driver.title
        assert "https://yuvanbank-qa-r1-test.netlify.app/forgot" in driver.current_url
        fp.verify_send_otp_btn_is_present()
        fp.enter_email_address(data["fpw_yb_valid"])
        fp.click_on_send_otp_button()
        Waiter(driver).visible(fp.SUCCESS_MSG_OTP_SEND_TEXT)

        #assert_equals("Enter OTP *", fp.otp_text_box_name(),"otp text box name is matching")
        #assert_equals("New password",fp.get_the_place_holder_Text(),"place holder text is matching")
        ##fp.enter_confirm_password(data["confrim_pass"])





