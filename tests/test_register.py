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
    @pytest.mark.parametrize("data", test_data)
    @pytest.mark.smoke
    def test_verify_register_functionality_with_valid_data(self, driver, data, env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()                 # includes waits

        rp.click_gender_male()
        rp.enter_first_name(data["FirstName"])
        rp.enter_last_name(data["LastName"])

        unique_email = f"{data['Email'].split('@')[0]}+{uuid.uuid4().hex[:6]}@{data['Email'].split('@')[1]}"
        rp.enter_email_address(unique_email)

        rp.enter_password(data["Password"])
        rp.enter_confirm_password(data["ConfirmPassword"])
        rp.click_register_button()

        rp.wait_visible(RegisterPage.RESULT_BANNER)
        assert_equals("Your registration completed", rp.get_result_text(), "Registration unsuccessful")
        rp.click_logout_link()

    @allure.story("Verify Register functionality with empty data")
    @pytest.mark.regression
    def test_verify_register_functionality_with_valid_data(self, driver,  env):
        hp = HomePage(driver, env)
        hp.open_home()

        rp = RegisterPage(driver, env)
        rp.open_register_page()                 # includes waits

        rp.click_gender_male()
        rp.enter_first_name("")
        rp.enter_last_name("")
        rp.enter_email_address("")

        rp.enter_password("")
        rp.enter_confirm_password("")
        rp.click_register_button()
