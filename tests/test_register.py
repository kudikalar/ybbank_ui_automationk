import allure
import pytest, uuid
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/register_test_data.xlsx")

@allure.feature("Registration")
class TestRegister:

    @allure.story("Verify Register functionality with valid data")
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    def test_register_valid_ddt(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()

        rp.click_gender_male()
        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])

        local, domain = data["Email"].split("@", 1)
        unique_email = f"{local}+{uuid.uuid4().hex[:6]}@{domain}"
        rp.enter_email_address(unique_email)

        rp.enter_password(data["Password"])
        rp.enter_confirm_password(data["ConfirmPassword"])
        rp.click_register_button()

        rp.wait_visible(RegisterPage.RESULT_BANNER)
        assert_equals("Your registration completed", rp.get_result_text(), "Registration unsuccessful")
        rp.click_logout_link()

    @allure.story("Verify Register functionality with empty data")
    @pytest.mark.regression
    def test_register_empty_fields_validation(self, driver, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()

        rp.click_gender_male()
        rp.enter_first_name("")
        rp.enter_last_name("")
        rp.enter_email_address("")
        rp.enter_password("")
        rp.enter_confirm_password("")
        rp.click_register_button()
        # add asserts for error messages if needed
