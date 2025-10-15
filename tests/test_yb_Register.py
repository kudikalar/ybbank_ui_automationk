import allure
import pytest

from core.wait import Waiter
from pages.Register_YB_Page import RegisterYBPage

from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/yb_login_test_data.xlsx")


@allure.feature("YB_Login")
class TestYBLogin:

    @allure.story("Login with valid credentials")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_login_with_valid_credentials(self, driver, data, env):
        rp = RegisterYBPage(driver, env)
        rp.open_register_page()

        rp.enter_full_name_yb(data["full_name"])
        rp.enter_email_address(data["email"])
        rp.enter_password(data["password"])
        rp.enter_confirm_pwd(data["confrim_pwd"])
        rp.click_register_sign_btn()

        Waiter(driver).visible(rp.VERIFY_LOGIN_PAGE)
        assert_equals(
            "Banking App",
            rp.verify_login_yb(),
            msg="User should see Banking App header after registration"
        )

        actual_title = rp.get_page_title()
        assert_equals(
            "Simple Banking App (Demo)",
            actual_title,
            msg="Page title should match expected"
        )




